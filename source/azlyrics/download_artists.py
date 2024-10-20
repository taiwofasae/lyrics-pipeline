import argparse
import os
import download_indexes
import sqlite3
from source.azlyrics import azlyrics, argparse_utils


def download(metadb, folderpath, indexletter = None, filepath = None):
    
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
        artists = azlyrics.artists(indexletter)
        #artists = ['tiwasavage','burnaboy','wizkid','tems','davido']
        
        for artist in artists:
            try:
                cur.execute("INSERT INTO artists (slug, artist_letter, url, status) VALUES (?, ?, ?, ?)", (artist, indexletter, '', 'pending'))
                con.commit()
            except Exception as e:
                print(f"Could not insert artist {artist} into artists table of db.")
                pass
        
        # update indexes download in db
        cur.execute("SELECT count(*) FROM artists WHERE artist_letter = ? and status!='done';", (indexletter,))
        not_dones = cur.fetchone()[0]
        if not_dones == 0:
            cur.execute("UPDATE indexes WHERE letter = ? set status = 'done';", (indexletter,))
            con.commit() 
        
        with open(os.path.join(folderpath, filepath), 'w') as f:
            f.write('\n'.join(artists))
            
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
    
    iteration = 0
    while iteration < args.tries:
        
        try:
            print('===========================================')
            print(f'Starting iteration number {iteration+1}...')
            download(args.metadatadb, args.folderpath, args.indexletter, args.filepath)
            print(f'..done!')
            break
        except AssertionError as e:
            pass
        
        iteration += 1
    
    
    
    
    
    