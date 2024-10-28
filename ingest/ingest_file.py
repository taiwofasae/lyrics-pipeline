import sqlite3
import numpy as np
import pandas as pd
from source import lyrics_helpers
import csv
import argparse
from ingest import ingest_file, artifact

def main(filename : str):
    df = artifact.load(filename)
    assert len(df.index) > 0, f"rows empty in {filename}"
    print(f"{len(df.index)} rows in {filename}")
    return df

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def save_to_db(db_filepath, df):
    con = sqlite3.connect(db_filepath)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS songs (ARTIST_NAME, ARTIST_URL, SONG_NAME, SONG_URL, LYRICS);")
    con.commit()
    
    for chunk in chunker(df, 10):
        try:
            cur.executemany("INSERT INTO songs (ARTIST_NAME, ARTIST_URL, SONG_NAME, SONG_URL, LYRICS) VALUES (?, ?, ?, ?, ?)", 
                        zip(chunk['ARTIST_NAME'].values, chunk['ARTIST_URL'].values, chunk['SONG_NAME'].values, chunk['SONG_URL'].values, chunk['LYRICS'].values))
            con.commit()

        except Exception as e:
            print(e)
    
    cur.execute("SELECT count(*) FROM songs;")
    total = cur.fetchone()[0]
    print(f"{total} rows now in db.")
    
    con.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '--inputfile','-i',
        type=str,
        required=True,
        help='Input file source')
    
    parser.add_argument(
        '--outputcsv','-o',
        type=str,
        required=False,
        help='Output csv file')
    
    parser.add_argument(
        '--sqlite','-db',
        type=str,
        required=False,
        help='Output sqlite file')
    
    args= parser.parse_args()
    
    df = main(args.inputfile)
    
    if args.outputcsv:
        artifact.create(df, args.outputcsv)
    
    if args.sqlite:
        save_to_db(args.sqlite, df)
        
