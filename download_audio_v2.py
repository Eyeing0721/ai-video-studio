"""Download ALL BGM and SFX tracks from API to media_library/ — v2

Key findings from investigation:
- Pixabay URLs with numeric IDs (e.g., ...-513668/) → scrape page → CDN download URL → download MP3
- Pixabay slug-only URLs (e.g., /music/ambient-dreams) → 14 of 17 are 404 (stale/dead links)
- SFX URLs are mostly search pages, not individual track pages
- Musopen PD tracks have download URLs on a different platform
- Some tracks (youtube_audio_library) have no URL

Uses curl with full browser headers to bypass Cloudflare protection.
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API_BASE = "http://127.0.0.1:8000/api"
MEDIA_ROOT = Path(r"C:\Users\Administrator\ai-video-studio\media_library")
BGM_DIR = MEDIA_ROOT / "bgm"
SFX_DIR = MEDIA_ROOT / "sfx"

CURL_ARGS = [
    "-sL", "--max-time", "15",
    "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "-H", "Accept-Language: en-US,en;q=0.5",
]

DL_ARGS = [
    "-sL", "--max-time", "120",
    "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "-H", "Accept: */*",
    "-H", "Accept-Language: en-US,en;q=0.5",
    "-H", "Referer: https://pixabay.com/",
]

class Stats:
    def __init__(self):
        self.downloaded = []      # (id, size_bytes)
        self.existing = []        # (id, path)
        self.no_url = []          # (id, name, reason)
        self.blocked = []         # (id, url)
        self.stale_url = []       # (id, url)
        self.no_cdn = []          # (id, url)
        self.failed = []          # (id, url, error)
        self.skipped_other = []   # (id, name, source)
stats = Stats()

def curl_get(url):
    """Fetch URL content."""
    cmd = ["curl"] + CURL_ARGS + [url]
    result = subprocess.run(cmd, capture_output=True, timeout=20)
    return result.stdout.decode("utf-8", errors="replace")

def curl_head(url):
    """Get HTTP headers."""
    cmd = ["curl", "-sI", "-L", "--max-time", "10",
           "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"]
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, timeout=15)
    return result.stdout.decode("utf-8", errors="replace")

def curl_download(url, dest):
    """Download file."""
    cmd = ["curl"] + DL_ARGS + ["-o", str(dest), url]
    result = subprocess.run(cmd, capture_output=True, timeout=130)
    return result.returncode == 0 and dest.exists()

def fetch_api(endpoint):
    """Fetch JSON from API."""
    result = subprocess.run(
        ["curl", "-s", f"{API_BASE}/{endpoint}"],
        capture_output=True, timeout=10
    )
    return json.loads(result.stdout.decode("utf-8", errors="replace"))

def check_url_status(url):
    """Check if a URL exists and get status."""
    headers = curl_head(url)
    statuses = re.findall(r'HTTP/\S+\s+(\d+)', headers)
    return statuses[-1] if statuses else "???"

def extract_cdn_url(html):
    """Extract Pixabay CDN download URL from page HTML."""
    if len(html) < 200:
        return None
    if "Just a moment..." in html:
        return "CLOUDFLARE_BLOCKED"
    # Pattern: cdn.pixabay.com/download/audio/YYYY/MM/DD/audio_HASH.mp3?filename=...
    matches = re.findall(
        r'https?://cdn\.pixabay\.com/download/audio/[^\s"\'<>]+\.mp3[^\s"\'<>]*',
        html
    )
    return matches[0] if matches else None

def has_numeric_id(url):
    return bool(re.search(r'-(\d{4,})/', url))

def try_download_track(track_id, cdn_url, dest_dir):
    """Try to download a track from a CDN URL."""
    dest = dest_dir / f"{track_id}.mp3"
    if dest.exists():
        stats.existing.append((track_id, str(dest)))
        print(f"    SKIP: already exists")
        return True

    print(f"    Downloading...")
    time.sleep(0.5)
    ok = curl_download(cdn_url, dest)
    if ok:
        size = dest.stat().st_size
        if size < 2000:
            print(f"    WARNING: file too small ({size} bytes), removing")
            dest.unlink()
            stats.failed.append((track_id, cdn_url, f"Too small ({size} bytes)"))
            return False
        stats.downloaded.append((track_id, size))
        print(f"    OK: {size / 1024:.1f} KB")
        return True
    else:
        stats.failed.append((track_id, cdn_url, "Download failed"))
        print(f"    FAILED")
        return False

def process_bgm(track):
    track_id = track["id"]
    name = track.get("name", "")
    url = track.get("url", "")
    download_url = track.get("download_url", "")
    source = track.get("source", "unknown")

    dest = BGM_DIR / f"{track_id}.mp3"
    if dest.exists():
        stats.existing.append((track_id, str(dest)))
        print(f"  SKIP [exists]: {name}")
        return

    effective_url = url or download_url
    if not effective_url:
        stats.no_url.append((track_id, name, f"No URL (source: {source})"))
        print(f"  SKIP [no URL]: {name} ({source})")
        return

    print(f"  Processing: {name} [{source}]")

    if "pixabay.com" in effective_url:
        if has_numeric_id(effective_url):
            print(f"    Pixabay numeric ID URL - scraping...")
            html = curl_get(effective_url)
            cdn = extract_cdn_url(html)
            if cdn == "CLOUDFLARE_BLOCKED":
                stats.blocked.append((track_id, effective_url))
                print(f"    BLOCKED by Cloudflare")
            elif cdn:
                print(f"    CDN: {cdn[:100]}...")
                try_download_track(track_id, cdn, BGM_DIR)
            else:
                stats.no_cdn.append((track_id, effective_url))
                print(f"    No CDN URL found")
        else:
            # Slug URL - check if it's stale
            status = check_url_status(effective_url)
            if status == "404":
                stats.stale_url.append((track_id, effective_url))
                print(f"    STALE (404): {effective_url}")
            elif status in ("200", "302", "301"):
                print(f"    Slug URL (HTTP {status}) - trying scrape...")
                html = curl_get(effective_url)
                cdn = extract_cdn_url(html)
                if cdn == "CLOUDFLARE_BLOCKED":
                    stats.blocked.append((track_id, effective_url))
                    print(f"    Cloudflare blocked")
                elif cdn:
                    try_download_track(track_id, cdn, BGM_DIR)
                else:
                    stats.no_cdn.append((track_id, effective_url))
                    print(f"    No CDN URL in page")
            else:
                stats.blocked.append((track_id, effective_url))
                print(f"    HTTP {status} (blocked/inaccessible)")

    elif any(d in effective_url for d in ["motionarray.com", "musopen.org", "freesound.org", "youtube"]):
        stats.skipped_other.append((track_id, name, source))
        print(f"    SKIP: {source} requires manual download")

    else:
        # Try direct download
        print(f"    Trying direct download: {effective_url[:80]}")
        # Check content type first
        headers = curl_head(effective_url)
        ct = re.search(r'(?i)content-type:\s*([^\r\n]+)', headers)
        ct_str = ct.group(1).strip().lower() if ct else "unknown"
        if "audio" in ct_str or "octet-stream" in ct_str or "mpeg" in ct_str:
            try_download_track(track_id, effective_url, BGM_DIR)
        else:
            stats.failed.append((track_id, effective_url, f"Not audio (Content-Type: {ct_str})"))
            print(f"    Not audio: {ct_str}")

def process_sfx(track):
    track_id = track["id"]
    name = track.get("name", "")
    url = track.get("url", "")
    source = track.get("source", "unknown")

    dest = SFX_DIR / f"{track_id}.mp3"
    if dest.exists():
        stats.existing.append((track_id, str(dest)))
        print(f"  SKIP [exists]: {name}")
        return

    if not url:
        stats.no_url.append((track_id, name, f"No URL (source: {source})"))
        print(f"  SKIP [no URL]: {name}")
        return

    print(f"  Processing: {name} [{source}]")

    # Check if the URL looks like a search/listing page
    if any(marker in url for marker in ["/search/", "/people/", "mixkit.co/free"]):
        stats.no_url.append((track_id, name, f"Search page: {url}"))
        print(f"    SKIP: Search/listing page")
        return

    # Check if it's a Pixabay numeric-ID URL
    if "pixabay.com" in url and has_numeric_id(url):
        print(f"    Pixabay numeric ID - scraping...")
        html = curl_get(url)
        cdn = extract_cdn_url(html)
        if cdn == "CLOUDFLARE_BLOCKED":
            stats.blocked.append((track_id, url))
            print(f"    Cloudflare blocked")
        elif cdn:
            try_download_track(track_id, cdn, SFX_DIR)
        else:
            stats.no_cdn.append((track_id, url))
            print(f"    No CDN URL")
    else:
        stats.no_url.append((track_id, name, f"Non-download URL ({source})"))
        print(f"    SKIP: Not a downloadable URL")

def print_report(bgm_total, sfx_total):
    print("\n" + "=" * 70)
    print("  DOWNLOAD REPORT")
    print("=" * 70)

    total = bgm_total + sfx_total
    dl_size = sum(d[1] for d in stats.downloaded)
    local = len(stats.downloaded) + len(stats.existing)

    print(f"\n  API: {bgm_total} BGM + {sfx_total} SFX = {total} tracks")

    print(f"\n  {'='*50}")
    print(f"  DOWNLOADED: {len(stats.downloaded)} files ({dl_size / (1024*1024):.1f} MB)")
    print(f"  {'='*50}")
    for tid, sz in stats.downloaded:
        print(f"    + {tid} ({sz / 1024:.1f} KB)")

    if stats.existing:
        print(f"\n  ALREADY EXIST: {len(stats.existing)} files")
        for tid, path in stats.existing:
            print(f"    ~ {tid}")

    if stats.stale_url:
        print(f"\n  STALE URLs (404 - Pixabay page removed): {len(stats.stale_url)}")
        for tid, url in stats.stale_url:
            print(f"    - {tid}")

    if stats.blocked:
        print(f"\n  BLOCKED (Cloudflare): {len(stats.blocked)}")
        for tid, url in stats.blocked:
            print(f"    X {tid}")

    if stats.no_cdn:
        print(f"\n  NO CDN URL FOUND: {len(stats.no_cdn)}")
        for tid, url in stats.no_cdn:
            print(f"    ? {tid}")

    if stats.no_url:
        print(f"\n  NO DOWNLOADABLE URL: {len(stats.no_url)}")
        for tid, name, reason in stats.no_url:
            print(f"    - {tid}: {name} [{reason[:70]}]")

    if stats.skipped_other:
        print(f"\n  OTHER PLATFORM: {len(stats.skipped_other)}")
        for tid, name, src in stats.skipped_other:
            print(f"    - {tid}: {name} ({src})")

    if stats.failed:
        print(f"\n  FAILED: {len(stats.failed)}")
        for tid, url, err in stats.failed:
            print(f"    X {tid}: {err}")

    print(f"\n  {'='*50}")
    print(f"  TOTAL LOCAL: {local} files ({len(stats.downloaded)} new + {len(stats.existing)} existing)")
    print(f"  TOTAL PENDING: {total - local} tracks need URL updates")
    print(f"  {'='*50}")

def main():
    print("=" * 70)
    print("  AI Video Studio - Audio Library Downloader v2")
    print("=" * 70)

    BGM_DIR.mkdir(parents=True, exist_ok=True)
    SFX_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[1/4] Fetching BGM list...")
    bgm = fetch_api("bgm")
    print(f"  {len(bgm)} BGM tracks")

    print("\n[2/4] Fetching SFX list...")
    sfx = fetch_api("sfx")
    print(f"  {len(sfx)} SFX tracks")

    print(f"\n[3/4] Processing {len(bgm)} BGM tracks...")
    for i, t in enumerate(bgm):
        print(f"\n  BGM [{i+1}/{len(bgm)}]", end="")
        process_bgm(t)

    print(f"\n[4/4] Processing {len(sfx)} SFX tracks...")
    for i, t in enumerate(sfx):
        print(f"\n  SFX [{i+1}/{len(sfx)}]", end="")
        process_sfx(t)

    print_report(len(bgm), len(sfx))

if __name__ == "__main__":
    main()
