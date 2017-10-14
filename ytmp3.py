"""Download YouTube links from a chrome bookmark folder and save as MP3s."""

import json
import re
import sh
# import eyed3
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

ydl = sh.Command("youtube-dl")


def is_bookmarks_folder(node):
    """True if the current node is the folder where YouTube links are stored."""
    return "name" in node and node["name"] == "ytmp3"


def get_time():
    """Return tuple of year and month as string for sorting files into folders."""
    # ts = link["date_added"]
    # dt = datetime.fromtimestamp(int(ts) / 10000000)
    dt = datetime.now()
    return str(dt.year), str(dt.month)


def get_ytid(link):
    """Return YouTube-ID for a YouTube link."""
    exp = ".+[/?&]v=(\w+)"
    match = re.match(exp, link["url"])

    if not match:
        click.echo("No ytid found for {}".format(link["url"]))
        return False
    else:
        return match.group(1)


def donwload_link(link, fname):
    """Download link using youtube-dl."""
    click.echo("Downloading {} at {}".format(link["name"], datetime.now()))
    cmd = YOUTUBE_PARAMS.split(" ") + ["-o", fname, link["url"]]
    output = ydl(cmd)
    outfile = extract_download_location(str(output))
    if outfile:
        click.echo("Completed at {}".format(outfile))
    else:
        click.echo("Download of {} failed".format(link["url"]))
    # write_mp3_tags(outfile)


# def write_mp3_tags(fname):
#     f = eyed3.load(fname)
#     f.tag.artist = artist
#     f.tag.title = title
#     f.tag.save()


def extract_download_location(output):
    """Extract final filename from youtube-dl shell output."""
    target = "[ffmpeg] Destination:"
    start = output.find(target)
    end = output.find("\n", start)
    try:
        return output[start + len(target):end]
    except TypeError:
        return False


def check_links(links):
    """Check all bookmarks in a folder and download all new YouTube links."""
    year, month = get_time()
    for link in links:
        ytid = get_ytid(link)
        if ytid:
            fpath = [MP3_FOLDER, year, month, FNAME_FORMAT]
            if not file_exists(ytid):
                donwload_link(link, path.sep.join(fpath))


def file_exists(ytid):
    """Check if a file for given YouTube-ID exists."""
    for (dirpath, dirnames, filenames) in walk(MP3_FOLDER):
        for f in filenames:
            if f.find(ytid) >= 0:
                return True
    return False


def run():
    with open(CHROME_BOOKMARKS, "rb") as f:
        bookmarks = json.load(f)

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
