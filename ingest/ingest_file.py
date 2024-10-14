import pandas as pd
from source import lyrics_helpers
import csv

def main(filename : str):
    # df = pd.read_csv(filename, index_col=0, quoting=csv.QUOTE_ALL)
    csv_list = lyrics_helpers.read_csv_max_split(filepath=filename)
    df = pd.DataFrame(csv_list[1:], columns=csv_list[0])
    return df, csv_list