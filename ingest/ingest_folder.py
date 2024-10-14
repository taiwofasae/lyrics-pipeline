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