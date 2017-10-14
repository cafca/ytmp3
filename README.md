# ytmp3

This script lets you save YouTube links to a Chrome bookmarks folder, which
are then automatically downloaded and converted to MP3s in a local folder on
your computer.

## Installation

Install dependencies

    $ brew install youtube-dl libav

Download and extract the (lastest ytmp3 release)[https://github.com/ciex/ytmp3/releases].

Optional:

Run in the background by changing the line in `crontab` file to point to
your installation directory and pasting it in your crontab with

    $ crontab -e


## Usage

Run

    $ ./dist/ytmp3

Script will download all links in the `ytmp3` folder in your Chrome bookmark
bar to the folder `~/Music/ytmp3/[year]/[month]/` as mp3 files.


## Environment setup (Mac)

Install deps

    $ brew install youtube-dl libav python3 pip

Setup environment and clone repo

    $ virtualenv -p python3 ytmp3
    $ cd ytmp3
    $ source bin/activate
    $ git clone https://github.com/ciex/ytmp3 src
    $ pip install -r src/requirements.txt
    
test with
    
    $ python src/ytmp3.py

Adapt and then add the line in the `cronjob` file to your crontab by executing `crontab -e`

## License

See the LICENSE file.

## Contributing

PRs are welcome. Send a message/email if you have questions.
