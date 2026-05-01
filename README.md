# musicbrainz-to-discogs

Automatically sync your MusicBrainz-tagged music library to your Discogs collection.

If you use [MusicBrainz Picard](https://github.com/metabrainz/picard) to tag your music, this script reads the embedded MusicBrainz Release IDs from your files, looks up the corresponding Discogs release via the MusicBrainz API and adds it to your Discogs collection – no manual searching required.

## Features

- supports FLAC, MP3, OGG, Opus, M4A
- scans your library folder recursively, one lookup per album
- resolves MusicBrainz Release IDs → Discogs Release IDs via the MusicBrainz API
- adds matched releases to your Discogs collection (folder: *Uncategorized*)
- dry-run mode to preview matches before making any changes
- respects MusicBrainz API rate limits (1 req/s)
- reports unmatched albums at the end for manual follow-up

## Requirements

- Python 3.8+
- a Discogs account with an API token
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

Open `mb2discogs.py` and set the following variables at the top:

```python
MUSIC_DIR        = "/path/to/your/music"
DISCOGS_TOKEN    = "your_discogs_token"   # discogs.com → Settings → Developers
DISCOGS_USERNAME = "your_username"
DRY_RUN          = True                   # set to False when ready
```

## Usage

```bash
# preview what would be added (safe, no changes made)
python mb2discogs.py

# actually add to your Discogs collection
# set DRY_RUN = False in the script first
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

## Limitations

- releases are always added to the "Uncategorized" folder; moving them into custom Discogs folders has to be done manually
- the script does not distinguish between physical (CD, vinyl) and digital releases yet; it simply matches whatever MusicBrainz links to Discogs
- if a release exists on Discogs but has no link in MusicBrainz, it won't be found automatically and has to be added manually

## Acknowledgements
This script was inspired by my friend [svetixoxo](https://github.com/svetixoxo), who wanted to sync her own MusicBrainz-tagged library to Discogs and sparked the idea to build a little tool for it.

## License

[MIT License](LICENSE)
