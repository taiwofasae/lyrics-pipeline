import string
from source.azlyrics import azlyrics, argparse_utils
import sqlite3


def download(metadb, filepath):
    # save to sqlite
    con = sqlite3.connect(metadb)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS indexes (letter primary key, status)")
    
    indexes = azlyrics.indexes()
    print(indexes)
    
    for ind in indexes:
        try:
            cur.execute("INSERT INTO indexes (letter, status) VALUES (?, ?)", (ind, 'pending'))
            con.commit()
        except Exception as e:
            print(f"Could not insert index {ind} into indexes table of db.")
            pass
    
    con.close()
    
    with open(filepath, 'w') as f:
        f.write('\n'.join(indexes))

if __name__ == '__main__':
    
    parser = argparse_utils.parser
    parser.add_argument(
        '--filepath',
        type=str,
        required=True,
        help='File path destination')
    
    args= parser.parse_args()
    
    download(args.metadatadb, args.filepath)
    

    
    
        
        
    
    