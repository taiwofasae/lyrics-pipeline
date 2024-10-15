from source.azlyrics import azlyrics, argparse_utils
import sqlite3

def download(metadb, artist, song, filepath):
    
    lyrics = azlyrics.lyrics(artist=artist, song=song)
    lyrics = lyrics[0] if lyrics else ''
    
    with open(filepath, 'w') as f:
        f.write(lyrics)
    
    # update song download in db
    con = sqlite3.connect(metadb)
    cur = con.cursor()
    cur.execute("UPDATE songs WHERE song = ? and artist = ? set status = 'done';", (song, artist))
    
    con.close()
    
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
    
    download(args.metadatadb, args.artist, args.song, args.filepath)
    
    