# yt-downloader

A simple command-line YouTube downloader built on [yt-dlp](https://github.com/yt-dlp/yt-dlp).

## Setup

```bash
pip install -r requirements.txt
```

[FFmpeg](https://ffmpeg.org/) is needed to merge high-quality video and audio streams and for `--audio` MP3 conversion.

## Usage

```bash
python yt_downloader.py <url> [<url> ...] [options]
```

| Option | Description |
| --- | --- |
| `-o, --output DIR` | Output directory (default: `downloads`) |
| `-a, --audio` | Download audio only, as MP3 |
| `-q, --quality HEIGHT` | Max video height, e.g. `1080`, `720`, `480` |
| `-p, --playlist` | Download the whole playlist if the URL is part of one |
| `-i, --info` | Show title, channel, duration and available qualities without downloading |

### Examples

```bash
python yt_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
python yt_downloader.py https://youtu.be/dQw4w9WgXcQ --audio
python yt_downloader.py https://youtu.be/dQw4w9WgXcQ -q 720 -o videos
python yt_downloader.py "https://www.youtube.com/playlist?list=..." --playlist
```

Only download content you have the right to download, and respect YouTube's Terms of Service.
