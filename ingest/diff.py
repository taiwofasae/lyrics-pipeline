import argparse

from ingest import artifact


def diff(df1, df2, df1_label='left_only', df2_label='right_only'):
    df1['duplicate_counter'] = df1.groupby(list(df1.columns)).cumcount()
    df2['duplicate_counter'] = df2.groupby(list(df2.columns)).cumcount()
    merged = df1.merge(df2, indicator=True, how='outer')
    
    merged['_merge'] = merged['_merge'].map({'left_only': df1_label,
                               'right_only': df2_label})
    return merged[merged['_merge'] != 'both']
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '--csv1','-c1',
        type=str,
        required=True,
        help='First csv file')
    
    parser.add_argument(
        '--csv2','-c2',
        type=str,
        required=True,
        help='Second csv file')
    
    args= parser.parse_args()
    
    
    
    df = diff(df1=artifact.load(args.csv1), df2=artifact.load(args.csv2), 
              df1_label=args.csv1, df2_label=args.csv2)
    
    df["LYRICS"] = df["LYRICS"].apply(lambda x: x[:20])
    print(f"{len(df.index)} different rows.")
    print(df.to_string())