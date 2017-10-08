# ytmp3

This script lets you save YouTube links to a Chrome bookmarks folder, which
are then automatically downloaded and converted to MP3s in a local folder on
your computer.

## Installation (Mac)

1. Install deps

    $ brew install youtube-dl libav python3 pip

2. Setup environment and clone repo

    $ virtualenv -p python3 ytmp3
    
    $ cd ytmp3
    
    $ source bin/activate
    
    $ git clone https://github.com/ciex/ytmp3 src
    
    $ pip install -r src/requirements.txt
    
    test with
    
    $ python src/ytmp3.py

3. Edit the `CHROME_BOOKSMARKS` and `MP3_FOLDER` variables in `ytmp3.py`, then
edit the first two lines in `start.sh`.

4. Add the line in the `cronjob` file to your crontab by executing `crontab -e`

## Issues

- Bookmark date is not converted correctly so that folder names don't reflect
    date of bookmark correctly

## License

See the LICENSE file.

## Contributing

PRs are welcome. Send a message/email if you have questions.
