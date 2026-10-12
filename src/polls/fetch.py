"""Download sources to data/raw/ exactly as received, with pinning and a manifest.

Nothing here parses content. Every download goes through `_download`, which
writes the bytes unchanged, computes a SHA-256 and appends a manifest row.
A download is skipped if its target file (whose name contains the pinned
identifier) already exists.
"""
from __future__ import annotations

import csv
import hashlib
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests
import yaml

USER_AGENT = (
    "strategic-voting-polls-2RS/0.1 "
    "(https://github.com/clarasalas/strategic-voting-polls-2RS; clara5salas2@gmail.com)"
)
MIN_DELAY_S = 1.5

MANIFEST_COLUMNS = [
    "source", "url", "pinned_id", "retrieved_utc", "sha256", "local_path", "archive_url",
]

WIKI_API = "https://fr.wikipedia.org/w/api.php"
WIKI_TITLE = "Liste de sondages sur l'élection présidentielle française de {year}"
ELECTIONS = (2002, 2007, 2012, 2017, 2022)


class PoliteSession:
    """requests.Session with a descriptive User-Agent and a minimum delay between requests."""

    def __init__(self, min_delay: float = MIN_DELAY_S):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self.min_delay = min_delay
        self._last = 0.0

    def get(self, url: str, **kwargs) -> requests.Response:
        wait = self.min_delay - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        kwargs.setdefault("timeout", 60)
        try:
            resp = self.session.get(url, **kwargs)
        finally:
            self._last = time.monotonic()
        resp.raise_for_status()
        return resp


# --------------------------------------------------------------------------- config

def load_sources(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


SOURCES_HEADER = (
    "# Pinned sources. A null pin is resolved (and written back here) on the next run\n"
    "# of notebooks/01_collect_and_parse.ipynb; existing pins are never changed automatically.\n"
)


def save_sources(cfg: dict, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(SOURCES_HEADER)
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)


def resolve_pins(cfg: dict, http: PoliteSession) -> list[str]:
    """Fill in any missing pinned identifiers (null in sources.yaml). Returns what was pinned.

    Existing pins are never changed; to update a pin, edit or blank it in sources.yaml.
    """
    pinned = []
    for year, entry in cfg["wikipedia"].items():
        if not entry.get("revision_id"):
            r = http.get(WIKI_API, params=dict(
                action="query", prop="revisions", rvprop="ids|timestamp",
                titles=entry["title"], format="json", formatversion=2,
            )).json()
            rev = r["query"]["pages"][0]["revisions"][0]
            entry["revision_id"] = int(rev["revid"])
            entry["revision_timestamp"] = rev["timestamp"]
            pinned.append(f"wikipedia {year}: {rev['revid']}")

    for key, kw in (("nsppolls", {"sha": "master"}), ("results", {})):
        entry = cfg[key]
        if not entry.get("commit"):
            params = {"per_page": 1, **kw}
            if key == "results":  # last commit that modified this file
                params["path"] = entry["path"]
            commits = http.get(
                f"https://api.github.com/repos/{entry['repo']}/commits", params=params
            ).json()
            entry["commit"] = commits[0]["sha"]
            entry["commit_date"] = commits[0]["commit"]["committer"]["date"]
            pinned.append(f"{key}: {entry['commit']}")
    return pinned


# --------------------------------------------------------------------------- manifest

def _append_manifest(manifest: Path, row: dict) -> None:
    new = not manifest.exists()
    with open(manifest, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MANIFEST_COLUMNS)
        if new:
            w.writeheader()
        w.writerow({k: row.get(k, "") for k in MANIFEST_COLUMNS})


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class EmptyResponse(Exception):
    pass


def _download(http, url, dest: Path, *, source, pinned_id, manifest, root,
              params=None, archive_url="", require_content=False) -> tuple[Path, bool]:
    """Write the response body to `dest` unchanged. Returns (path, downloaded?)."""
    if dest.exists():
        return dest, False
    dest.parent.mkdir(parents=True, exist_ok=True)
    resp = http.get(url, params=params)
    if require_content and not resp.content:
        raise EmptyResponse(f"empty response from {url}")
    tmp = dest.with_suffix(dest.suffix + ".part")
    tmp.write_bytes(resp.content)
    tmp.rename(dest)
    _append_manifest(manifest, dict(
        source=source, url=resp.url, pinned_id=pinned_id,
        retrieved_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        sha256=sha256(dest), local_path=str(dest.relative_to(root)), archive_url=archive_url,
    ))
    return dest, True


# --------------------------------------------------------------------------- sources

def raw_paths(cfg: dict, raw_dir: Path) -> dict:
    """Where each pinned source lives under data/raw/. Used by both downloading and
    parsing, so parsing can locate files without any network access."""
    fp, nsp, res = cfg["france_politique"], cfg["nsppolls"], cfg["results"]
    ts = fp.get("wayback_timestamp")
    return {
        "wikipedia": {int(y): raw_dir / "wikipedia" / f"{y}_rev{e['revision_id']}.json"
                      for y, e in cfg["wikipedia"].items()},
        "france_politique": raw_dir / "france_politique" / fp["filename"],
        "france_politique_wayback": raw_dir / "france_politique" / f"wayback_{ts}_{fp['filename']}" if ts else None,
        "nsppolls": raw_dir / "nsppolls" / f"{nsp['commit'][:12]}_{Path(nsp['path']).name}",
        "results": raw_dir / "results" / f"{res['commit'][:12]}_{Path(res['path']).name}",
    }


def fetch_wikipedia(cfg, http, raw_dir: Path, manifest: Path, root: Path) -> dict[int, Path]:
    """action=parse on the pinned revision; the API JSON response is archived as-is."""
    paths = raw_paths(cfg, raw_dir)["wikipedia"]
    for year, entry in cfg["wikipedia"].items():
        rev = entry["revision_id"]
        _download(
            http, WIKI_API, paths[int(year)], source=f"wikipedia_{year}", pinned_id=rev,
            manifest=manifest, root=root,
            params=dict(action="parse", oldid=rev, prop="text|revid|displaytitle",
                        format="json", formatversion=2),
        )
    return paths


def request_wayback_snapshot(http: PoliteSession, url: str) -> str | None:
    """Ask the Wayback Machine to capture `url` now. Returns the 14-digit timestamp of
    the capture, or None if Save Page Now did not answer with one."""
    try:
        resp = http.get(f"https://web.archive.org/save/{url}", timeout=180, allow_redirects=False)
    except requests.RequestException:
        return None
    m = re.search(r"/web/(\d{14})/", resp.headers.get("Location", "") + resp.headers.get("Content-Location", ""))
    return m.group(1) if m else None


def wayback_url(ts: str, url: str, raw: bool = False) -> str:
    """raw=True gives the capture exactly as archived, without the Wayback toolbar."""
    return f"https://web.archive.org/web/{ts}{'id_' if raw else ''}/{url}"


def fetch_france_politique(cfg, http, raw_dir, manifest, root) -> dict[str, Path | None]:
    """Live page, plus the Wayback capture of it (pinned by its timestamp in sources.yaml).

    If no timestamp is pinned yet, a capture is requested and its timestamp written to
    cfg (the caller saves sources.yaml). The capture may take a few minutes to become
    downloadable; until then its copy is skipped and retried on the next run.
    """
    entry = cfg["france_politique"]
    if not entry.get("wayback_timestamp"):
        entry["wayback_timestamp"] = request_wayback_snapshot(http, entry["url"])
    ts = entry.get("wayback_timestamp")
    paths = raw_paths(cfg, raw_dir)
    archive = wayback_url(ts, entry["url"]) if ts else ""
    _download(http, entry["url"], paths["france_politique"], source="france_politique_2002",
              pinned_id=f"wayback:{ts}" if ts else "", manifest=manifest, root=root, archive_url=archive)
    if ts and not paths["france_politique_wayback"].exists():
        try:
            _download(http, wayback_url(ts, entry["url"], raw=True), paths["france_politique_wayback"],
                      source="france_politique_2002_wayback", pinned_id=f"wayback:{ts}",
                      manifest=manifest, root=root, archive_url=archive, require_content=True)
        except (requests.RequestException, EmptyResponse) as e:
            print(f"Wayback capture {ts} not downloadable yet ({e}); will retry on the next run.")
    return {k: v for k, v in paths.items() if k.startswith("france_politique")}


def _github_raw(repo, commit, path):
    return f"https://raw.githubusercontent.com/{repo}/{commit}/{quote(path)}"


def fetch_nsppolls(cfg, http, raw_dir, manifest, root) -> Path:
    e = cfg["nsppolls"]
    dest = raw_paths(cfg, raw_dir)["nsppolls"]
    _download(http, _github_raw(e["repo"], e["commit"], e["path"]), dest,
              source="nsppolls_2022", pinned_id=e["commit"], manifest=manifest, root=root)
    return dest


def fetch_results(cfg, http, raw_dir, manifest, root) -> Path:
    e = cfg["results"]
    dest = raw_paths(cfg, raw_dir)["results"]
    _download(http, _github_raw(e["repo"], e["commit"], e["path"]), dest,
              source="results", pinned_id=e["commit"], manifest=manifest, root=root)
    return dest
