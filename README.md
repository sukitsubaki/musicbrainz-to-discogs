# musicbrainz-to-discogs
Automatically sync your MusicBrainz-tagged music library to your Discogs collection.

If you use [MusicBrainz Picard](https://github.com/metabrainz/picard) to tag your music, this script reads the embedded MusicBrainz Release IDs from your files, looks up the corresponding Discogs release via the MusicBrainz API and adds it to your Discogs collection — no manual searching required.

## Features

- supports MP3, FLAC, OGG, Opus, M4A
- scans your library folder recursively, one lookup per album
- resolves MusicBrainz Release IDs to Discogs Release IDs via the MusicBrainz API
- adds matched releases to your Discogs collection (folder: *Uncategorized*)
- dry-run mode to preview matches before making any changes
- respects MusicBrainz API rate limits (1 req/s)
- reports unmatched albums at the end for manual follow-up

## Requirements

- Python 3.8+
- a discogs account with an API token
- music tagged with MusicBrainz Picard (so files have a `musicbrainz_albumid` tag)

## Installation

```bash
git clone https://github.com/sukitsubaki/musicbrainz-to-discogs.git
cd musicbrainz-to-discogs

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration

Open `musicbrainz-to-discogs.py` and set the following variables at the top:

```python
MUSIC_DIR       = "/path/to/your/music"
DISCOGS_TOKEN   = "your_discogs_token"     # discogs.com → Settings → Developers
DISCOGS_USERNAME = "your_discogs_username"
DRY_RUN         = True                     # set to False when ready
```

## Usage

```bash
# Preview what would be added (safe, no changes made)
python musicbrainz-to-discogs.py

# Actually add to your Discogs collection
# (set DRY_RUN = False in the script first)
python musicbrainz-to-discogs.py
```

### Example output

```
🔍 Scanning music directory: /home/user/Music

📀 1035 unique albums found.

[1/1035] Definitely Maybe
  MB-ID: ef927fa4-2f6b-4431-8867-0573b0e9c234
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
- **Runtime**: ~1 second per album due to API rate limiting (1.000 albums ≈ 17 minutes)
- **Duplicates**: Already-added releases are skipped gracefully
- **macOS users**: `._` AppleDouble metadata files are automatically ignored

## License

[MIT License](LICENSE)
