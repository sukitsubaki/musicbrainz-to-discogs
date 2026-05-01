# musicbrainz-to-discogs

Automatically sync your MusicBrainz-tagged music library to your Discogs collection.

If you use [MusicBrainz Picard](https://github.com/metabrainz/picard) to tag your music, this script reads the embedded MusicBrainz Release IDs from your files, looks up the corresponding Discogs release via the MusicBrainz API and adds it to your Discogs collection – no manual searching required.

## Features

- Supports FLAC, MP3, OGG, Opus, M4A
- Scans your library folder recursively, one lookup per album
- Resolves MusicBrainz Release IDs → Discogs Release IDs via the MusicBrainz API
- Adds matched releases to your Discogs collection (folder: *Uncategorized*)
- Dry-run mode to preview matches before making any changes
- Respects MusicBrainz API rate limits (1 req/s)
- Reports unmatched albums at the end for manual follow-up

## Requirements

- Python 3.8+
- A Discogs account with an API token
- Music tagged with MusicBrainz Picard (so files have a `musicbrainz_albumid` tag)

## Installation

```bash
git clone https://github.com/sukitsubaki/musicbrainz-to-discogs.git
cd musicbrainz-to-discogs

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Open `mb2discogs.py` and set the following variables at the top:

```python
MUSIC_DIR       = "/path/to/your/music"
DISCOGS_TOKEN   = "your_discogs_token"   # discogs.com → Settings → Developers
DISCOGS_USERNAME = "your_username"
DRY_RUN         = True                   # set to False when ready
```

## Usage

```bash
# Preview what would be added (safe, no changes made)
python mb2discogs.py

# Actually add to your Discogs collection
# (set DRY_RUN = False in the script first)
python mb2discogs.py
```

### Example output

```
🔍 Scanning music directory: /home/user/Music

📀 1035 unique albums found.

[1/1035] Definitely Maybe
  MB-ID: 9ab6fec-efda-3ad0-9316-92af1575a31d
  Discogs-ID: 368093
  ✓ Added: Definitely Maybe

==================================================
✅ Matched: 812/1035
❌ No Discogs link: 223

Albums not found (add manually on Discogs):
  - ...  [MB: https://musicbrainz.org/release/...]
```

## Notes

- **Match rate**: Typically over 80 % of releases will have a Discogs link in MusicBrainz. Niche, self-released or very obscure releases often don't.
- **Runtime**: ~1 second per album due to API rate limiting (1.000 albums ≈ 17 minutes).
- **Duplicates**: Already-added releases are skipped gracefully.
- **macOS users**: `._` AppleDouble metadata files are automatically ignored.

## Acknowledgements
This script was inspired by my friend [svetixoxo](https://github.com/svetixoxo), who wanted to sync her own MusicBrainz-tagged library to Discogs and sparked the idea to build a little tool for it.

## License

[MIT License](LICENSE)
