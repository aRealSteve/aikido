#!/usr/bin/env python3
"""A simple YouTube downloader built on top of yt-dlp.

Examples:
    python yt_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
    python yt_downloader.py URL --audio                 # MP3 audio only
    python yt_downloader.py URL --quality 720 -o videos  # max 720p into ./videos
    python yt_downloader.py URL --info                  # show info, don't download
"""

import argparse
import sys

try:
    from yt_dlp import YoutubeDL
    from yt_dlp.utils import DownloadError
except ImportError:
    sys.exit("yt-dlp is not installed. Run: pip install -r requirements.txt")


def build_options(output_dir, audio_only=False, quality=None, playlist=False):
    """Translate the CLI flags into yt-dlp options."""
    opts = {
        "outtmpl": f"{output_dir}/%(title)s [%(id)s].%(ext)s",
        "noplaylist": not playlist,
        "progress_hooks": [_progress_hook],
        "quiet": True,
        "no_warnings": True,
    }

    if audio_only:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    else:
        height = f"[height<={quality}]" if quality else ""
        opts["format"] = f"bestvideo{height}+bestaudio/best{height}/best"
        opts["merge_output_format"] = "mp4"

    return opts


def _progress_hook(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\r  {percent:>7}  {speed:>12}  ETA {eta}", end="", flush=True)
    elif d["status"] == "finished":
        print(f"\r  Downloaded: {d['filename']}" + " " * 10)


def show_info(url):
    with YoutubeDL({"quiet": True, "no_warnings": True, "noplaylist": True}) as ydl:
        info = ydl.extract_info(url, download=False)
    duration = info.get("duration") or 0
    print(f"Title:    {info.get('title')}")
    print(f"Channel:  {info.get('uploader')}")
    print(f"Duration: {duration // 60}:{duration % 60:02d}")
    print(f"Views:    {info.get('view_count')}")
    heights = sorted({f["height"] for f in info.get("formats", []) if f.get("height")})
    if heights:
        print(f"Qualities: {', '.join(f'{h}p' for h in heights)}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Download YouTube videos or audio.")
    parser.add_argument("urls", nargs="+", help="one or more video/playlist URLs")
    parser.add_argument("-o", "--output", default="downloads",
                        help="output directory (default: downloads)")
    parser.add_argument("-a", "--audio", action="store_true",
                        help="download audio only and convert to MP3")
    parser.add_argument("-q", "--quality", type=int, metavar="HEIGHT",
                        help="max video height, e.g. 1080, 720, 480")
    parser.add_argument("-p", "--playlist", action="store_true",
                        help="download the whole playlist if the URL has one")
    parser.add_argument("-i", "--info", action="store_true",
                        help="print video info without downloading")
    args = parser.parse_args(argv)

    failed = 0
    for url in args.urls:
        try:
            if args.info:
                show_info(url)
                continue
            print(f"Downloading {url}")
            opts = build_options(args.output, args.audio, args.quality, args.playlist)
            with YoutubeDL(opts) as ydl:
                ydl.download([url])
        except DownloadError:
            # yt-dlp has already printed the error message.
            failed += 1
        except KeyboardInterrupt:
            sys.exit("\nCancelled.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
