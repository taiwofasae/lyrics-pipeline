import argparse
import os
import download_indexes
import sqlite3
from source.azlyrics import azlyrics, argparse_utils, azlyrics_helpers


def download(metadb, folderpath, indexletter = None, filepath = None, tries = 1):
    
    # save to sqlite
    con = sqlite3.connect(metadb)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS artists (slug STRING primary key, artist_letter, url, status, foreign key (artist_letter) references indexes(letter));")
    
    indexes = [indexletter]
    filepaths = [filepath or f'{indexletter}.txt']
    if not indexletter:
        
        # fetch pending indexes
        cur.execute("SELECT letter FROM indexes WHERE status!='done';")
        indexes = [x[0] for x in cur.fetchall()]   
        
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
        
        for artist, url in artists:
            
            try:
                cur.execute("INSERT INTO artists (slug, artist_letter, url, status) VALUES (?, ?, ?, ?)", (artist, indexletter, url, 'pending'))
                con.commit()
            except Exception as e:
                print(f"Could not insert artist {artist} into artists table of db.")
                print(e)
        
        # update indexes download in db
        cur.execute("SELECT count(*) FROM artists WHERE artist_letter = ? and status!='done';", (indexletter,))
        not_dones = cur.fetchone()[0]
        if not_dones == 0:
            cur.execute("UPDATE indexes set status = 'done' WHERE letter = ?;", (indexletter,))
            con.commit() 
        
        with open(os.path.join(folderpath, filepath), 'w') as f:
            f.write('\n'.join([f"{artist},{url}" for artist, url in artists]))
            
    con.close()

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
    
    
    
    
    
    