from enum import Enum
import pandas as pd
import csv
import os

from source import lyrics_helpers


class ArtifactType(Enum):
    sqlite = 1
    csv = 2

def create(artifact : pd.DataFrame, storage_path : str):
    
    storage_path = storage_path if os.path.splitext(storage_path)[1] else f"{storage_path}.csv"
    artifact.to_csv(storage_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
    
    return storage_path

def load(storage_path : str, type = 'csv') -> pd.DataFrame:
    
    csv_list = lyrics_helpers.read_csv_max_split(filepath=storage_path)
    return pd.DataFrame(csv_list[1:], columns=csv_list[0])

def append(destination : str, artifact : pd.DataFrame):
    
    dest_df = load(destination)
    
    df = pd.concat([dest_df, artifact], ignore_index=True)
    
    return create(artifact=df, storage_path=destination)
    