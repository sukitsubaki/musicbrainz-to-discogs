"""
MusicBrainz → Discogs Collection Importer
==========================================
github.com/sukitsubaki/musicbrainz-to-discogs

Requirements:
    pip install mutagen requests

Discogs API token:
    Discogs → Settings → Developers → "Generate new token"
"""

import os
import time
import requests
import mutagen
from mutagen.flac import FLAC
from mutagen.id3 import ID3

# ─── Configuration ────────────────────────────────────────────────────────────

MUSIC_DIR        = "/path/to/your/music"
DISCOGS_TOKEN    = "YOUR_DISCOGS_TOKEN"
DISCOGS_USERNAME = "YOUR_DISCOGS_USERNAME"

# set to "False" when ready to write to your Discogs collection
DRY_RUN = True

# ─── Constants ────────────────────────────────────────────────────────────────

MB_API_URL  = "https://musicbrainz.org/ws/2/release/{mbid}?inc=url-rels&fmt=json"
MB_HEADERS  = {"User-Agent": "musicbrainz-to-discogs/1.0 (github.com/sukitsubaki/musicbrainz-to-discogs)"}
DISCOGS_URL = "https://api.discogs.com/users/{username}/collection/folders/1/releases/{release_id}"
AUDIO_EXTS  = (".mp3", ".flac", ".ogg", ".opus", ".m4a", ".aac", ".mp4")

# ─── Functions ────────────────────────────────────────────────────────────────

def get_mbid_from_file(filepath):
    """Read the MusicBrainz Release ID from an audio file's tags."""
    try:
        ext = filepath.lower().rsplit(".", 1)[-1]
        if ext == "flac":
            audio = FLAC(filepath)
            return audio.get("musicbrainz_albumid", [None])[0]
        elif ext == "mp3":
            audio = ID3(filepath)
            for tag in audio.values():
                if hasattr(tag, "desc") and "album id" in tag.desc.lower():
                    return tag.text[0] if tag.text else None
        elif ext in ("m4a", "aac", "mp4", "ogg", "opus"):
            audio = mutagen.File(filepath)
            if audio is None:
                return None
            val = audio.get("----:com.apple.iTunes:MusicBrainz Album Id") \
                or audio.get("musicbrainz_albumid")
            if val:
                v = val[0]
                return v.decode() if isinstance(v, bytes) else v
    except Exception as e:
        print(f"  ⚠ Tag error: {os.path.basename(filepath)}: {e}")
    return None


def get_discogs_id_from_mbid(mbid):
    """Look up the Discogs Release ID linked to a MusicBrainz Release ID."""
    try:
        r = requests.get(MB_API_URL.format(mbid=mbid), headers=MB_HEADERS, timeout=10)
        r.raise_for_status()
        for rel in r.json().get("relations", []):
            url_str = rel.get("url", {}).get("resource", "")
            if "discogs.com/release/" in url_str:
                return int(url_str.rstrip("/").split("/")[-1])
    except Exception as e:
        print(f"  ⚠ MusicBrainz API error ({mbid}): {e}")
    return None


def add_to_discogs_collection(discogs_id, title):
    """Add a release to the Discogs collection (folder: Uncategorized)."""
    if DRY_RUN:
        print(f"  [DRY RUN] Would add: {title} (Discogs ID {discogs_id})")
        return True
    try:
        r = requests.post(
            DISCOGS_URL.format(username=DISCOGS_USERNAME, release_id=discogs_id),
            headers={
                "Authorization": f"Discogs token={DISCOGS_TOKEN}",
                "User-Agent": MB_HEADERS["User-Agent"],
            },
            timeout=10,
        )
        if r.status_code in (200, 201):
            print(f"  ✓ Added: {title}")
            return True
        elif r.status_code == 409:
            print(f"  – Already in collection: {title}")
            return True
        else:
            print(f"  ✗ Discogs error {r.status_code}: {r.text}")
    except Exception as e:
        print(f"  ✗ Request error: {e}")
    return False


def collect_unique_mbids(music_dir):
    """Walk the music directory and collect one MBID per album folder."""
    seen, results = set(), []
    for root, _, files in os.walk(music_dir):
        for fname in sorted(files):
            if not fname.lower().endswith(AUDIO_EXTS):
                continue
            if fname.startswith("._"):  # skip macOS AppleDouble files
                continue
            mbid = get_mbid_from_file(os.path.join(root, fname))
            if mbid and mbid not in seen:
                seen.add(mbid)
                results.append((mbid, root))
                break  # one file per folder is enough
    return results

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"🔍 Scanning music directory: {MUSIC_DIR}\n")
    albums = collect_unique_mbids(MUSIC_DIR)
    print(f"📀 {len(albums)} unique albums found.\n")

    matched, not_found = 0, []

    for i, (mbid, folder) in enumerate(albums, 1):
        title = os.path.basename(folder)
        print(f"[{i}/{len(albums)}] {title}")
        print(f"  MB ID: {mbid}")

        discogs_id = get_discogs_id_from_mbid(mbid)

        if discogs_id:
            print(f"  Discogs ID: {discogs_id}")
            add_to_discogs_collection(discogs_id, title)
            matched += 1
        else:
            print(f"  – No Discogs link found in MusicBrainz")
            not_found.append((mbid, title))

        time.sleep(1.1)  # MusicBrainz rate limit: max 1 req/s

    print(f"\n{'=' * 50}")
    print(f"✅ Matched:       {matched}/{len(albums)}")
    print(f"❌ No Discogs link: {len(not_found)}")

    if not_found:
        print("\nAlbums not found — add manually on Discogs:")
        for mbid, name in not_found:
            print(f"  - {name}")
            print(f"    https://musicbrainz.org/release/{mbid}")

if __name__ == "__main__":
    main()
