# -*- coding: utf-8 -*-

import os
import sqlite3
from shutil import copyfile

PROFILE_LOCATION = '/Users/pv/Library/Application Support/Firefox/Profiles/twspts81.default'

class FirefoxScanner:
    def __enter__(self):
        self.places_db = self.connect_db()
        return self

    def __exit__(self, *args, **kwargs):
        self.places_db.close()
        os.remove(self.db_fname)
        os.remove(self.db_fname + '-shm')
        os.remove(self.db_fname + '-wal')

    def connect_db(self):
        self.make_db_copy()
        return sqlite3.connect(self.db_fname)

    def make_db_copy(self):
        # create a copy of the db on each run to avoid errors if firefox
        # is currently running and accessing the db
        original_db_fname = os.path.join(PROFILE_LOCATION, 'places.sqlite')
        self.db_fname = os.path.join(PROFILE_LOCATION, 'places-temp-ytmp3.sqlite')
        copyfile(original_db_fname, self.db_fname)

    def marshall_results(self, results):
        # marshall the return value to have the same shape as chrome bookmarks
        # json
        return [{"url": r[0]} for r in results]

    def run(self):
        # moz_places contains the urls but does not record in which folder
        # the bookmark is stored. the folders are stored in moz_bookmarks
        # and linked via moz_bookmarks.fk = moz_places.id
        query = """
            select moz_places.url from moz_places 
            inner join moz_bookmarks on moz_bookmarks.fk = moz_places.id
            where moz_bookmarks.parent = 
                (select id from moz_bookmarks 
                where title='ytmp3' 
                order by parent asc 
                limit 1);
        """
        results = self.places_db.execute(query)
        return self.marshall_results(results)

if __name__ == '__main__':
    with FirefoxScanner() as scanner:
        print(scanner.run())