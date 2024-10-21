from source.azlyrics import azlyrics, argparse_utils
import os
import sqlite3

def main(artist_slug : str):
    # file_man = file_manager.File('../data')
    # with open(file_man('azlyrics/taylorswift.html'), 'r') as f:
    #     taylorswift = f.read()
    #songs = azlyrics.songs(artist=artist_slug, html_content=taylorswift)
    songs = azlyrics.songs(artist=artist_slug)
    
    return songs['songs']

def download(metadb, artist, filepath):
    # save to sqlite
    con = sqlite3.connect(metadb)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS songs (title, artist, url, status, primary key (title, artist), foreign key (artist) references artists(slug));")
    
    # fetch pending artists
    cur.execute("SELECT slug FROM artists WHERE status!='done' limit 200;")
    artists = [x[0] for x in cur.fetchall()]  
    
    # or force fetch all artists
    
        
    songs = azlyrics.songs(artist=artist)['songs']
    assert len(songs) > 0, "songs list is empty"
    
    for title, url in songs:
        try:
            cur.execute("INSERT INTO songs (title, artist, url, status) VALUES (?, ?, ?, ?)", (title, artist, url, 'pending'))
            con.commit()

        except Exception as e:
            print(f"Could not insert song {title} into songs table of db.")
    
    # update artist download in db
    cur.execute("SELECT count(*) FROM songs WHERE artist = ? and status!='done';", (artist,))
    not_dones = cur.fetchone()[0]
    if not_dones == 0:
        cur.execute("UPDATE artists set status = 'done' WHERE slug = ? ;", (artist))
        con.commit()
    
            
    with open(filepath, 'w') as f:
        f.write('\n'.join([f'{title}|{url}' for title,url in songs]))
        
    con.close()
    
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
        
        iteration += 1
    
    
    
    