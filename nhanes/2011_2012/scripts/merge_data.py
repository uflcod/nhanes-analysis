#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pds

def main():
    demo_df = pds.read_table('../refined_data/demographics.tsv',  index_col='SEQN')
    nhanescog_df = pds.read_csv('../data/nhanescog_2011_12_CSV.csv', index_col='seqn')
    nhanescog_df.index.name = 'SEQN' # change index name for merging
    perio_df = pds.read_table('../refined_data/perio_summary.tsv', index_col='SEQN')
    tobacco_df = pds.read_table('../refined_data/tobacco.tsv', index_col='SEQN')

    # merge cognitive and perio data
    merged_df = nhanescog_df.merge(perio_df, how='inner', on='SEQN')
    print('cognitive and perio merge len:', len(merged_df))

    # merge demographic, cognitive, and perio data
    merged_df = \
        demo_df.merge(merged_df, how='inner', on='SEQN')
    print('demographics, cognitive, and perio merge len:', len(merged_df))

    # drop NaNs
    merged_df = merged_df.dropna()
    print('drop NANs merge len:', len(merged_df))
    
    # merge in tobacco data
    merged_df = merged_df.merge(tobacco_df, how='left', on='SEQN')
    print('tobacco merge len:', len(merged_df))

    # set index to SEQN
    # merged_df.set_index('SEQN')
    return merged_df

if __name__ == "__main__":
    df = main()
    # print(df.head()) # testing
    df.to_csv('../refined_data/merged_data.tsv', sep='\t')