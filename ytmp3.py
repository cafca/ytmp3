import json
import re
import sh
from os import path, walk
from datetime import datetime

CHROME_BOOKMARKS = "/Users/vaul/Library/Application Support/Google/Chrome/Default/Bookmarks"
MP3_FOLDER = "/Users/vaul/Music/ytmp3"
YOUTUBE_COMMAND = "-f bestaudio --extract-audio --audio-format mp3 --audio-quality 320 --no-playlist".split(" ")

ydl = sh.Command("youtube-dl")


def is_bookmarks_folder(node):
    return "name" in node and node["name"] == "ytmp3"


def get_time(link):
    ts = link["date_added"]
    dt = datetime.fromtimestamp(int(ts) / 10000000)
    return str(dt.year), str(dt.month)


def get_ytid(link):
    exp = ".+[/?&]v=(\w+)"
    match = re.match(exp, link["url"])

    if not match:
        print("No ytid found for {}".format(link["url"]))
        return False
    else:
        return match.group(1)


def donwload_link(link, fname):
    print("Downloading {}".format(link["name"]))
    cmd = YOUTUBE_COMMAND + ["-o", fname, link["url"]]
    ydl(cmd)


def check_links(links):
    print("Checking {} links".format(len(links)))
    for link in links:
        year, month = get_time(link)
        ytid = get_ytid(link)
        if ytid:
            print("{} - {}: {}".format(year, month, ytid))
            fn = [MP3_FOLDER, year, month, "%(title)s_%(id)s_%(ext)s.%(ext)s"]
            if not file_exists(fn, ytid):
                donwload_link(link, path.sep.join(fn))


def file_exists(fn, ytid):
    p = path.sep.join(fn[:-1])
    for (dirpath, dirnames, filenames) in walk(p):
        for f in filenames:
            if f.find(ytid) >= 0:
                return True
    return False


if __name__ == "__main__":
    with open(CHROME_BOOKMARKS, "r") as f:
        bookmarks = json.load(f)

    try:
        bookmark_bar = bookmarks["roots"]["bookmark_bar"]["children"]
    except KeyError:
        print("Create ytmp3 bookmark")

    for node in bookmark_bar:
        if is_bookmarks_folder(node):
            check_links(node["children"])
