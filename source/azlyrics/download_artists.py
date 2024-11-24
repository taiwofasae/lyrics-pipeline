import argparse
import contextlib
import os
import download_indexes
import sqlite3
from source.azlyrics import azlyrics, argparse_utils, azlyrics_helpers

class DB:
    
    def create_table_if_not_exist(metadb):
        with contextlib.closing(sqlite3.connect(metadb)) as db_con:
            cur = db_con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS artists (slug STRING primary key, artist_letter, url, status, foreign key (artist_letter) references indexes(letter));")
            db_con.commit()
            
    def fetch_pending_indexes(metadb):
        indexes = []
        with contextlib.closing(sqlite3.connect(metadb)) as db_con:
            cur = db_con.cursor()
            # fetch pending indexes
            cur.execute("SELECT letter FROM indexes WHERE status!='done';")
            indexes = [x[0] for x in cur.fetchall()]  
            
        return indexes
    
    def insert_artists_into_db(db_con, artists, indexletter):
        cur = db_con.cursor()
        for artist, url in artists:
            
            try:
                # todo: use indexletter from url instead
                cur.execute("INSERT INTO artists (slug, artist_letter, url, status) VALUES (?, ?, ?, ?)", (artist, indexletter, url, 'pending'))
                db_con.commit()
            except Exception as e:
                print(f"Could not insert artist {artist} into artists table of db.")
                print(e)
                
    def update_indexes_table_on_complete(db_con, indexletter):
        cur = db_con.cursor()
        # update indexes download in db
        cur.execute("SELECT count(*) FROM artists WHERE artist_letter = ? and status!='done';", (indexletter,))
        not_dones = cur.fetchone()[0]
        if not_dones == 0:
            cur.execute("UPDATE indexes set status = 'done' WHERE letter = ?;", (indexletter,))
            db_con.commit() 

def download(metadb, folderpath, indexletter = None, filepath = None, tries = 1):
    
    
    indexes = [indexletter]
    filepaths = [filepath or f'{indexletter}.txt']
    if not indexletter:
        indexes = DB.fetch_pending_indexes(metadb)
         
        
        # or force fetch all indexes
        # indexes = download_indexes.main()
         
        filepaths = [f'{ind}.txt' for ind in indexes]
        
    folderpath = args.folderpath
    
    for indexletter, filepath in zip(indexes, filepaths):
        
        trie = 0
        while trie < tries:
            
            try:
                print(f'Try #{trie+1}...')
                artists = [(azlyrics_helpers.get_artist_slug(url), url) for artist, url in azlyrics.artists(indexletter)]
                
                assert len(artists ) > 0, "artists list is empty"
                break
            except AssertionError as e:
                print(e)
            
            trie += 1
        
        
        
        #artists = ['tiwasavage','burnaboy','wizkid','tems','davido']
        if metadb:
            with contextlib.closing(sqlite3.connect(metadb)) as db_con:
                
                # insert artists into db
                DB.insert_artists_into_db(db_con, artists, indexletter)
                
                # update indexes table on complete
                DB.update_indexes_table_on_complete(db_con, indexletter)
        
        
        with open(os.path.join(folderpath, filepath), 'w') as f:
            f.write('\n'.join([f"{artist},{url}" for artist, url in artists]))
            

if __name__ == '__main__':
    
    parser = argparse_utils.parser
    
    parser.add_argument(
        '--indexletter',
        type=str,
        required=False,
        help='Artist letter index')
    
    parser.add_argument(
        '--folderpath',
        type=str,
        required=True,
        help='Folder path destination')
    
    parser.add_argument(
        '--filepath',
        type=str,
        required=False,
        help='File path destination')
    
    args= parser.parse_args()
    
    download(args.metadatadb, args.folderpath, args.indexletter, args.filepath, args.tries)
    
    
    
    
    
    