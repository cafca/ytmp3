"""Download YouTube links from a chrome bookmark folder and save as MP3s."""

import json
import re
import sh
import eyed3
from os import path, walk
from datetime import datetime

#
# brew install youtube-dl ffmpeg libmagic
#

# Location of Chrome bookmarks file (JSON format)
CHROME_BOOKMARKS = "/Users/vaul/Library/Application Support/Google/Chrome/Default/Bookmarks"

# Destination folder mp3s will be saved to
MP3_FOLDER = "/Users/vaul/Music/ytmp3"

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
        print("No ytid found for {}".format(link["url"]))
        return False
    else:
        return match.group(1)


def donwload_link(link, fname):
    """Download link using youtube-dl."""
    print("Downloading {} at {}".format(link["name"], datetime.now()))
    cmd = YOUTUBE_PARAMS.split(" ") + ["-o", fname, link["url"]]
    output = ydl(cmd)
    # outfile = extract_download_location(str(output))
    # write_mp3_tags(outfile)


def write_mp3_tags(fname):
    f = eyed3.load(fname)
    f.tag.artist = artist
    f.tag.title = title
    f.tag.save()


def extract_download_location(output):
    """Extract final filename from youtube-dl shell output."""
    start = output.find("[ffmpeg] Destination:")
    end = output.find("\n", start)
    return output[start, end]


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
    """Check if a file for given YouTube-ID exists at path."""
    for (dirpath, dirnames, filenames) in walk(MP3_FOLDER):
        for f in filenames:
            if f.find(ytid) >= 0:
                return True
    return False


if __name__ == "__main__":
    with open(CHROME_BOOKMARKS, "rb") as f:
        bookmarks = json.load(f)

    try:
        bookmark_bar = bookmarks["roots"]["bookmark_bar"]["children"]
    except KeyError:
        print("Create 'ytmp3' bookmark in your bookmark bar and put links in it!")
        quit()

    for node in bookmark_bar:
        if is_bookmarks_folder(node):
            check_links(node["children"])
