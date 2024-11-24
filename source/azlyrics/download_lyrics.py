from requests import TooManyRedirects
from source.azlyrics import azlyrics, argparse_utils
import sqlite3

def update_songs_db(metadb, artist, song):
    # update song download in db
    con = sqlite3.connect(metadb)
    cur = con.cursor()
    cur.execute("UPDATE songs set status = 'done' WHERE slug = ? and artist = ? ;", (song, artist))
    con.commit()
    con.close()

def download(metadb, artist, song, filepath):
    song = song.strip() if song else ''
    if not song:
        raise ValueError(f"Song value is empty: '{song}'")
    
    lyrics = azlyrics.lyrics(artist=artist, song=song)
    lyrics = lyrics[0] if lyrics else ''
    
    assert lyrics, 'lyrics is empty'
    
    with open(filepath, 'w') as f:
        f.write(lyrics)
    
    if metadb:
        update_songs_db(metadb, artist, song)
    
    
if __name__ == '__main__':
    parser = argparse_utils.parser
    
    parser.add_argument(
        '--artist',
        type=str,
        required=True,
        help='Artist slug')
    
    parser.add_argument(
        '--song',
        type=str,
        required=True,
        help='Song slug')
    
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
            
            download(args.metadatadb, args.artist, args.song, args.filepath)
            print(f'..done!')
            break
        except AssertionError as e:
            print(e)
        except TooManyRedirects as e:
            print("Too many redirects occurred.")
        except sqlite3.OperationalError as e:
            print(e)
            print("Trying sqlite update again ....")
            update_songs_db(args.metadatadb, args.artist, args.song)
        
        iteration += 1
    
    
    
    