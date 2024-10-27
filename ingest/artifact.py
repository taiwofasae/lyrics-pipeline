from enum import Enum
import pandas as pd
import csv
import os


class ArtifactType(Enum):
    sqlite = 1
    csv = 2

def create(artifact : pd.DataFrame, storage_path : str):
    
    storage_path = storage_path if os.path.splitext(storage_path)[1] else f"{storage_path}.csv"
    artifact.to_csv(storage_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    
    return storage_path

def load(storage_path : str, type = 'csv') -> pd.DataFrame:
    
    return pd.read_csv(storage_path, index_col=0)

def append(destination : str, artifact : pd.DataFrame):
    
    dest_df = load(destination)
    
    df = pd.concat([dest_df, artifact], ignore_index=True)
    
    return create(artifact=df, storage_path=destination)
    