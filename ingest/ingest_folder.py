import argparse
import csv
import os
import pandas as pd

from ingest import artifact, ingest_file

def main(folder_path : str, actifact_dest_path : str = None, extension_filter = ''):
    
    total_df = None
    for filename in os.listdir(folder_path):
        
        
        local_path = os.path.join(folder_path, filename).replace("\\","/")
        
        if not os.path.isfile(local_path):
            continue
        
        # filter for extension
        if not local_path.endswith(tuple(extension_filter.replace(';',',').split(','))):
            continue

        try:
            df = ingest_file.main(local_path)
        
            # append to artifact or create if not exist
            if total_df is None:
                total_df = df
            else:
                total_df = artifact.append_to(total_df, df)
                
            if actifact_dest_path:
                artifact.create(total_df, actifact_dest_path)
        except Exception as e:
            print(e)
            print(f"Ingesting failed for file: {local_path}")
    
    return total_df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '--folder','-f',
        type=str,
        required=True,
        help='Input folder')
    
    parser.add_argument(
        '--ext','-e',
        type=str,
        required=False,
        default='',
        help='File extension filter')
    
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
    
    df = main(args.folder, actifact_dest_path=args.outputcsv, extension_filter=args.ext)
    
    if df is None:
        print(f"No data found.")
        quit()
        
    print(f"{len(df.index)} rows in total.")
    
    if args.outputcsv:
        artifact.create(df, args.outputcsv)
        
    if args.sqlite:
        ingest_file.save_to_db(args.sqlite, df)
    
