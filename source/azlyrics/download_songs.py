from source.azlyrics import azlyrics, argparse_utils
import os
import sqlite3
from requests.exceptions import TooManyRedirects
import contextlib

class DB:
    
    def create_table_if_not_exist(metadb):
        with contextlib.closing(sqlite3.connect(metadb)) as db_con:
            cur = db_con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS songs (title, slug, artist, url, status, primary key (title, artist), foreign key (artist) references artists(slug));")
            db_con.commit()
            
    def insert_song_into_db(metadb, artist, title, url, slug=None, db_con=None):
        
        if db_con: # use existing cursor
            cursor = db_con.cursor()
            url = url or ''
            slug = slug or (url.split("/")[-1]).split('.html')[0]
            
            try:
                cursor.execute("INSERT INTO songs (title, slug, artist, url, status) VALUES (?, ?, ?, ?, ?)", (title, slug, artist, url, 'pending'))
                if db_con:
                    db_con.commit()

            except Exception as e:
                print(f"Could not insert song {title} into songs table of db.")
                
        else: # make new connection
            with contextlib.closing(sqlite3.connect(metadb)) as db_con:
                DB.insert_song_into_db(metadb, artist, title, url, db_con=db_con)
            
    def insert_songs_into_db(metadb, artist, songs):
        with contextlib.closing(sqlite3.connect(metadb)) as db_con:
            for title, url in songs:
                DB.insert_song_into_db(metadb, artist, title, url, db_con=db_con)
            
            DB.update_artists_table_on_complete(db_con, artist)
            
    def insert_songs_into_db1(metadb, artist, songs):
        with contextlib.closing(sqlite3.connect(metadb)) as db_con:
            cur = db_con.cursor()
            for title, url in songs:
                url = url or ''
                slug = url.split("/")[-1]
                slug = slug.split('.html')[0]
                try:
                    cur.execute("INSERT INTO songs (title, slug, artist, url, status) VALUES (?, ?, ?, ?, ?)", (title, slug, artist, url, 'pending'))
                    db_con.commit()

                except Exception as e:
                    print(f"Could not insert song {title} into songs table of db.")
            
            DB.update_artists_table_on_complete(db_con, artist)
        
    def update_artists_table_on_complete(db_con, artist):
        cur = db_con.cursor()
        # update artist download in db
        cur.execute("SELECT count(*) FROM songs WHERE artist = ? and status!='done';", (artist,))
        not_dones = cur.fetchone()[0]
        if not_dones == 0:
            cur.execute("UPDATE artists set status = 'done' WHERE slug = ? ;", (artist))
            db_con.commit()

def main(artist_slug : str):
    # file_man = file_manager.File('../data')
    # with open(file_man('azlyrics/taylorswift.html'), 'r') as f:
    #     taylorswift = f.read()
    #songs = azlyrics.songs(artist=artist_slug, html_content=taylorswift)
    songs = azlyrics.songs(artist=artist_slug)
    
    return songs['songs']

def save_songs_to_file(filepath, songs):
    with open(filepath, 'w') as f:
        f.write('\n'.join([f'{title}|{url}' for title,url in songs]))
        
def read_songs_from_file(filepath):
    with open(filepath, 'r') as f:
        lines = [line.split('|') for line in f]
        
    return lines

def download(metadb, artist, filepath):
    
    # fetch pending artists
    #cur.execute("SELECT slug FROM artists WHERE status!='done' limit 200;")
    #artists = [x[0] for x in cur.fetchall()]  
    
    # or force fetch all artists
    
        
    songs = azlyrics.songs(artist=artist)['songs']
    assert len(songs) > 0, "songs list is empty"
    
    if metadb:
        DB.insert_songs_into_db(metadb, artist, songs)
    
    
    save_songs_to_file(filepath=filepath, songs=songs)
        
    
    
if __name__ == '__main__':
        
    parser = argparse_utils.parser
    
    parser.add_argument(
        '--artist',
        type=str,
        required=True,
        help='Artist slug')
    
    parser.add_argument(
        '--filepath',
        type=str,
        required=True,
        help='File path destination')
    
    args= parser.parse_args()
    
    if args.metadatadb:
        DB.create_table_if_not_exist(args.metadatadb)
    
    iteration = 0
    while iteration < args.tries:
        
        try:
            print(f'{args.tags}')
            print(f'Trying... #{iteration+1}...')
            
            download(args.metadatadb, args.artist, args.filepath)
            print(f'..done!')
            break
        except AssertionError as e:
            print(e)
        except TooManyRedirects as e:
            print("Too many redirects occurred.")
        
        iteration += 1
        
    
    
    
    
    