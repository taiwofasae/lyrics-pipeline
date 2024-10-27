import argparse
import csv
import os
import pandas as pd

from ingest import artifact, ingest_file

def main(folder_path : str, actifact_dest_path : str = None):
    
    total_df = None
    for root,dirs,files in os.walk(folder_path):
        for file in files:
            
            local_path = os.path.join(root, file).replace("\\","/")

            try:
                df, csv_list = ingest_file.main(local_path)
            
                # append to artifact or create if not exist
                if total_df is None:
                    total_df = df
                else:
                    total_df = pd.concat([total_df, df], ignore_index=True)
                    
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
    
    df = main(args.folder, actifact_dest_path=args.outputcsv)
    print(f"{len(df.index)} rows in total.")
    
    if args.outputcsv:
        df.to_csv(args.outputcsv, index=False, quoting=csv.QUOTE_NONNUMERIC)
        
    if args.sqlite:
        ingest_file.save_to_db(args.sqlite, df)
    