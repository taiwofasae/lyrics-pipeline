from source.azlyrics import azlyrics, argparse_utils
import os
import sqlite3
from requests.exceptions import TooManyRedirects

class DB:
    def create_table_if_not_exist(db_con):
        cur = db_con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS songs (title, slug, artist, url, status, primary key (title, artist), foreign key (artist) references artists(slug));")
        
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

def download(db_con, artist, filepath):
    
    # fetch pending artists
    #cur.execute("SELECT slug FROM artists WHERE status!='done' limit 200;")
    #artists = [x[0] for x in cur.fetchall()]  
    
    # or force fetch all artists
    
        
    songs = azlyrics.songs(artist=artist)['songs']
    assert len(songs) > 0, "songs list is empty"
    
    cur = db_con.cursor()
    for title, url in songs:
        slug = url.split("/")[-1]
        slug = slug.split('.html')[0]
        try:
            cur.execute("INSERT INTO songs (title, slug, artist, url, status) VALUES (?, ?, ?, ?, ?)", (title, slug, artist, url, 'pending'))
            db_con.commit()

        except Exception as e:
            print(f"Could not insert song {title} into songs table of db.")
    
    DB.update_artists_table_on_complete(db_con, artist)
    
    db_con.close()
            
    with open(filepath, 'w') as f:
        f.write('\n'.join([f'{title}|{url}' for title,url in songs]))
        
    
    
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
    
    db_con = sqlite3.connect(args.metadatadb)
    DB.create_table_if_not_exist(db_con)
    
    iteration = 0
    while iteration < args.tries:
        
        try:
            print(f'{args.tags}')
            print(f'Trying... #{iteration+1}...')
            
            download(db_con, args.artist, args.filepath)
            print(f'..done!')
            break
        except AssertionError as e:
            print(e)
        except TooManyRedirects as e:
            print("Too many redirects occurred.")
        finally:
            db_con.close()
        
        iteration += 1
    
    
    
    