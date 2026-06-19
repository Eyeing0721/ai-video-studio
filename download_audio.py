"""Download ALL BGM and SFX tracks from the API to media_library/

Strategy per URL type:
- Pixabay pages with numeric ID (e.g., ...-513668/) → scrape for CDN download URL → download
- Pixabay pages without numeric ID (slug only) → try scraping, may get Cloudflare block
- Pixabay sound-effects search pages → skip (not individual tracks)
- Empty URLs → skip
- Musopen pages → skip (different platform)
- Motionarray pages → skip (different platform)
- Freesound/other → skip (search pages, not individual tracks)

Uses curl for HTTP (bypasses Python urllib Cloudflare issues).
"""
import json
import os
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

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"

# Track results
class Stats:
    def __init__(self):
        self.downloaded = []      # (id, size_bytes, path)
        self.existing = []        # (id, path)
        self.no_url = []          # (id, name, source)
        self.no_cdn = []          # (id, url, reason)
        self.dl_failed = []       # (id, url, error)
        self.page_blocked = []    # (id, url)
        self.not_audio = []       # (id, url, content_type)

stats = Stats()

def curl_get(url, referer=None, output_file=None, timeout=30):
    """Fetch URL using curl. If output_file is given, download to file."""
    cmd = ["curl", "-sL", "--max-time", str(timeout),
           "-H", f"User-Agent: {UA}"]
    if referer:
        cmd += ["-H", f"Referer: {referer}"]
    if output_file:
        cmd += ["-o", str(output_file)]
    cmd.append(url)

    result = subprocess.run(cmd, capture_output=not bool(output_file), timeout=timeout + 5)
    if output_file:
        return result.returncode == 0
    else:
        return result.stdout.decode("utf-8", errors="replace")

def curl_head(url):
    """Get headers for a URL."""
    cmd = ["curl", "-sI", "-L", "--max-time", "10",
           "-H", f"User-Agent: {UA}"]
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, timeout=15)
    headers = result.stdout.decode("utf-8", errors="replace")
    return headers

def fetch_api(endpoint):
    """Fetch JSON from the API."""
    result = subprocess.run(
        ["curl", "-s", f"{API_BASE}/{endpoint}"],
        capture_output=True, timeout=10
    )
    return json.loads(result.stdout.decode("utf-8", errors="replace"))

def extract_cdn_download_url(page_url):
    """Scrape a Pixabay track page to find the CDN download URL.

    Success tested with numeric-ID URLs like:
    https://pixabay.com/music/adventure-total-war-epic-action-cinematic-trailer-main-513668/

    Returns the CDN download URL or None.
    """
    html = curl_get(page_url)
    if not html or len(html) < 200:
        return None

    # Check for Cloudflare block
    if "Just a moment..." in html or "cf-mitigated" in html.lower():
        return "CLOUDFLARE_BLOCKED"

    # Pattern: cdn.pixabay.com/download/audio/YYYY/MM/DD/audio_HASH.mp3?filename=...
    matches = re.findall(
        r'https?://cdn\.pixabay\.com/download/audio/[^\s"\'<>]+\.mp3[^\s"\'<>]*',
        html
    )
    if matches:
        return matches[0]

    # Fallback: any MP3 on cdn.pixabay.com
    matches = re.findall(
        r'https?://cdn\.pixabay\.com/[^\s"\'<>]+\.mp3[^\s"\'<>]*',
        html
    )
    if matches:
        return matches[0]

    return None

def has_numeric_id(url):
    """Check if a Pixabay URL has a numeric track ID."""
    return bool(re.search(r'-(\d{4,})/', url))

def download_file(url, dest_path):
    """Download a file to dest_path. Returns True on success."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    if dest_path.exists():
        return "EXISTS"

    print(f"    Downloading...")
    success = curl_get(url, referer="https://pixabay.com/", output_file=dest_path, timeout=120)

    if success and dest_path.exists():
        size = dest_path.stat().st_size
        if size < 1000:
            # Too small - probably an error page
            text = dest_path.read_text(encoding="utf-8", errors="replace")[:200]
            print(f"    WARNING: File too small ({size} bytes). Content: {text[:100]}")
            dest_path.unlink()
            return f"TOO_SMALL_{size}"
        print(f"    OK: {size / 1024:.1f} KB")
        return size
    return "CURL_FAILED"

def check_content_type(url):
    """Check if a URL returns audio content."""
    headers = curl_head(url)
    ct_match = re.search(r'(?i)content-type:\s*([^\r\n]+)', headers)
    if ct_match:
        ct = ct_match.group(1).strip()
        return ct
    return "unknown"

def process_bgm(track):
    """Process a single BGM track."""
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
        stats.no_url.append((track_id, name, source))
        print(f"  SKIP [no URL]: {name} (source: {source})")
        return

    print(f"  Processing: {name} [{source}]")

    # Strategy depends on URL type
    if "pixabay.com" in effective_url:
        if has_numeric_id(effective_url):
            print(f"    Pixabay URL with numeric ID - scraping for CDN link...")
            time.sleep(0.5)
            cdn_url = extract_cdn_download_url(effective_url)
            if cdn_url == "CLOUDFLARE_BLOCKED":
                stats.page_blocked.append((track_id, effective_url))
                print(f"    FAIL: Cloudflare blocked")
                return
            elif cdn_url:
                print(f"    Found CDN: {cdn_url[:100]}...")
                result = download_file(cdn_url, dest)
                if isinstance(result, int):
                    stats.downloaded.append((track_id, result, str(dest)))
                else:
                    stats.dl_failed.append((track_id, cdn_url, result))
            else:
                stats.no_cdn.append((track_id, effective_url, "No CDN URL found in page"))
                print(f"    FAIL: No CDN URL found")
        else:
            # Slug-only URL - try scraping but expect issues
            print(f"    Pixabay slug URL - attempting scrape...")
            time.sleep(0.5)
            cdn_url = extract_cdn_download_url(effective_url)
            if cdn_url == "CLOUDFLARE_BLOCKED":
                stats.page_blocked.append((track_id, effective_url))
                print(f"    FAIL: Cloudflare blocked")
            elif cdn_url:
                print(f"    Found CDN: {cdn_url[:100]}...")
                result = download_file(cdn_url, dest)
                if isinstance(result, int):
                    stats.downloaded.append((track_id, result, str(dest)))
                else:
                    stats.dl_failed.append((track_id, cdn_url, result))
            else:
                stats.no_cdn.append((track_id, effective_url, "No CDN URL (slug URL)"))
                print(f"    FAIL: No CDN URL (slug-only URL)")

    elif "motionarray.com" in effective_url:
        stats.no_url.append((track_id, name, f"Motionarray: {effective_url}"))
        print(f"    SKIP: Motionarray requires different download method")

    elif "musopen.org" in effective_url:
        stats.no_url.append((track_id, name, f"Musopen: {effective_url}"))
        print(f"    SKIP: Musopen requires different download method")

    elif "freesound.org" in effective_url:
        stats.no_url.append((track_id, name, f"Freesound: {effective_url}"))
        print(f"    SKIP: Freesound requires different download method")

    else:
        # Unknown URL - try direct download
        print(f"    Trying direct download...")
        ct = check_content_type(effective_url)
        if "audio" in ct.lower() or "octet-stream" in ct.lower():
            result = download_file(effective_url, dest)
            if isinstance(result, int):
                stats.downloaded.append((track_id, result, str(dest)))
            else:
                stats.dl_failed.append((track_id, effective_url, result))
        else:
            stats.not_audio.append((track_id, effective_url, ct))
            print(f"    NOT audio (Content-Type: {ct})")

def process_sfx(track):
    """Process a single SFX track."""
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
        stats.no_url.append((track_id, name, source))
        print(f"  SKIP [no URL]: {name} (source: {source})")
        return

    print(f"  Processing: {name} [{source}]")
    print(f"    URL: {url}")

    # Most SFX URLs are search pages, not individual tracks
    if "search/" in url or url.endswith("/") and not has_numeric_id(url):
        stats.no_url.append((track_id, name, f"Search page: {url}"))
        print(f"    SKIP: Search page URL, not individual track")
        return

    # Try scraping if it's a Pixabay page with numeric ID
    if "pixabay.com" in url and has_numeric_id(url):
        print(f"    Pixabay with numeric ID - scraping...")
        time.sleep(0.5)
        cdn_url = extract_cdn_download_url(url)
        if cdn_url == "CLOUDFLARE_BLOCKED":
            stats.page_blocked.append((track_id, url))
            print(f"    FAIL: Cloudflare blocked")
        elif cdn_url:
            result = download_file(cdn_url, dest)
            if isinstance(result, int):
                stats.downloaded.append((track_id, result, str(dest)))
            else:
                stats.dl_failed.append((track_id, cdn_url, result))
        else:
            stats.no_cdn.append((track_id, url, "No CDN URL"))
    else:
        stats.no_url.append((track_id, name, f"Non-download URL: {url}"))
        print(f"    SKIP: URL is not a direct download")


def print_report(bgm_count, sfx_count):
    print("\n" + "=" * 70)
    print("  DOWNLOAD REPORT")
    print("=" * 70)

    total_downloaded_size = sum(d[1] for d in stats.downloaded)
    total_tracks = bgm_count + sfx_count

    print(f"\n  API totals: {bgm_count} BGM + {sfx_count} SFX = {total_tracks} tracks")

    if stats.downloaded:
        print(f"\n  *** DOWNLOADED: {len(stats.downloaded)} files "
              f"({total_downloaded_size / (1024*1024):.1f} MB total) ***")
        for track_id, size, path in stats.downloaded:
            print(f"    + {track_id} ({size / 1024:.1f} KB)")
    else:
        print(f"\n  DOWNLOADED: 0 files")

    if stats.existing:
        print(f"\n  ALREADY EXIST: {len(stats.existing)} files")
        for track_id, path in stats.existing:
            print(f"    ~ {track_id}")

    if stats.no_url:
        print(f"\n  NO DOWNLOADABLE URL: {len(stats.no_url)} tracks")
        for track_id, name, reason in stats.no_url:
            print(f"    - {track_id}: {name} [{reason[:60]}]")

    if stats.no_cdn:
        print(f"\n  CDN URL NOT FOUND: {len(stats.no_cdn)} tracks")
        for track_id, url, reason in stats.no_cdn:
            print(f"    X {track_id}: {reason}")

    if stats.page_blocked:
        print(f"\n  PAGE BLOCKED (Cloudflare): {len(stats.page_blocked)} tracks")
        for track_id, url in stats.page_blocked:
            print(f"    BLOCKED {track_id}")

    if stats.dl_failed:
        print(f"\n  DOWNLOAD FAILED: {len(stats.dl_failed)} tracks")
        for track_id, url, error in stats.dl_failed:
            print(f"    FAIL {track_id}: {error}")

    if stats.not_audio:
        print(f"\n  NOT AUDIO: {len(stats.not_audio)} tracks")
        for track_id, url, ct in stats.not_audio:
            print(f"    NA {track_id}: {ct}")

    effectively_have = len(stats.downloaded) + len(stats.existing)
    print(f"\n  *** TOTAL LOCAL FILES: {effectively_have} "
          f"(downloaded: {len(stats.downloaded)}, pre-existing: {len(stats.existing)}) ***")


def main():
    print("=" * 70)
    print("  AI Video Studio - Audio Library Downloader")
    print("=" * 70)

    BGM_DIR.mkdir(parents=True, exist_ok=True)
    SFX_DIR.mkdir(parents=True, exist_ok=True)

    print("\n[1/4] Fetching BGM list...")
    bgm_list = fetch_api("bgm")
    print(f"  Got {len(bgm_list)} BGM tracks")

    print("\n[2/4] Fetching SFX list...")
    sfx_list = fetch_api("sfx")
    print(f"  Got {len(sfx_list)} SFX tracks")

    print(f"\n[3/4] Processing {len(bgm_list)} BGM tracks...")
    for i, track in enumerate(bgm_list):
        print(f"\n  BGM [{i+1}/{len(bgm_list)}] ", end="")
        process_bgm(track)

    print(f"\n[4/4] Processing {len(sfx_list)} SFX tracks...")
    for i, track in enumerate(sfx_list):
        print(f"\n  SFX [{i+1}/{len(sfx_list)}] ", end="")
        process_sfx(track)

    print_report(len(bgm_list), len(sfx_list))


if __name__ == "__main__":
    main()
