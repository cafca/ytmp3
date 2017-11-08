"""Download YouTube links from a chrome bookmark folder and save as MP3s."""

import json
import re
import youtube_dl
import click
from os import path, walk
from datetime import datetime
from time import sleep
from pathlib import Path

#
# brew install youtube-dl ffmpeg libmagic
#

home = str(Path.home())

# Location of Chrome bookmarks file (JSON format)
CHROME_BOOKMARKS = path.sep.join([home, "Library/Application Support/Google/Chrome/Default/Bookmarks"])

# Destination folder mp3s will be saved to
MP3_FOLDER = path.sep.join([home, "Music", "ytmp3"])

# Parameters for youtube-dl script
YOUTUBE_PARAMS = "-f bestaudio --extract-audio --audio-format mp3 --audio-quality 320 --add-metadata --embed-thumbnail --no-playlist"

# File name pattern for mp3 using youtube-dl format option
FNAME_FORMAT = "%(title)s (%(abr)sk)_%(id)s_%(ext)s.%(ext)s"


def is_bookmarks_folder(node):
    """True if the current node is the folder where YouTube links are stored."""
    return "name" in node and node["name"] == "ytmp3"


def target_path():
    """Return os specific target path for output files."""
    dt = datetime.now()
    return path.sep.join([
        MP3_FOLDER,
        str(dt.year),
        str(dt.month),
        FNAME_FORMAT
    ])


def get_ytid(link):
    """Return YouTube-ID for a YouTube link."""
    exp = ".+[/?&]v=(\w+)"
    match = re.match(exp, link["url"])

    if not match:
        click.echo("No ytid found for {}".format(link["url"]))
        return False
    else:
        return match.group(1)


def donwload_links(links):
    """Download links using youtube-dl."""
    click.echo("Downloading {} links".format(len(links)))

    class DownloadLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            click.echo("[WARNING] {}".format(msg))

        def error(self, msg):
            click.echo("[ERROR] {}".format(msg))

    youtube_params = {
        'format': 'bestaudio/best',
        'forcetitle': True,
        'writethumbnail': True,
        'noplaylist': True,
        'outtmpl': target_path(),
        'progress_hooks': [show_download_progress],
        'logger': DownloadLogger(),
        'postprocessors': [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"},
            {"key": "MetadataFromTitle", "titleformat": '%(artist)s - %(title)s'},
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'}
        ]
    }

    with youtube_dl.YoutubeDL(youtube_params) as ydl:
        ydl.download([link["url"] for link in links])


def show_download_progress(progress):
    """Show status of finished/failed downloads as they occur."""
    if progress["status"] == 'finished':
        click.echo("Download of {} finished. Now converting to mp3...".format(progress["filename"]))
    elif progress["status"] == 'error':
        click.echo("Download of {} failed\n\n{}".format(progress["filename"], progress))
    else:
        pass


def check_links(links):
    """Check all bookmarks in a folder and download all new YouTube links."""
    to_download = []
    for link in links:
        ytid = get_ytid(link)
        if ytid and not file_exists(ytid):
            to_download.append(link)
    if (len(to_download)) == 0:
        click.echo("Didn't find any new links to download")
    else:
        donwload_links(to_download)


def file_exists(ytid):
    """Check if a file for given YouTube-ID exists."""
    for (dirpath, dirnames, filenames) in walk(MP3_FOLDER):
        for f in filenames:
            if f.find(ytid) >= 0:
                return True
    return False


def run():
    try:
        with open(CHROME_BOOKMARKS, "rb") as f:
            bookmarks = json.load(f)
    except FileNotFoundError:
        click.echo("Couldn't find Google Chrome bookmarks at {}. Is it installed?".format(CHROME_BOOKMARKS))

    try:
        bookmark_bar = bookmarks["roots"]["bookmark_bar"]["children"]
    except KeyError:
        click.echo("Create 'ytmp3' bookmark in your bookmark bar and put links in it!")
        quit()

    for node in bookmark_bar:
        if is_bookmarks_folder(node):
            check_links(node["children"])


@click.command()
@click.option('--loop/--no-loop',
    default=False,
    help="Auto checking every 5 minutes.")
def main(loop):
    click.echo("Starting ytmp3...")
    if loop:
        try:
            while True:
                run()
                sleep(10)
        except KeyboardInterrupt:
            click.echo("\nGoodbye!")
    else:
        run()


if __name__ == "__main__":
    main()
