#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pds

def main():
    demo_df = pds.read_table('../refined_data/demographics.tsv',  index_col='SEQN')
    nhanescog_df = pds.read_csv('../data/nhanescog_2011_12_CSV.csv', index_col='seqn')
    nhanescog_df.index.name = 'SEQN' # change index name for merging
    perio_df = pds.read_table('../refined_data/perio_summary.tsv', index_col='SEQN')
    tobacco_df = pds.read_table('../refined_data/tobacco.tsv')

    # merge demographic, cognitive, and perio data
    merged_df = \
        demo_df.merge(
            nhanescog_df.merge(perio_df, how='inner', on='SEQN'),
            how='inner',
            on='SEQN'
        )

    # drop NaNs
    merged_df = merged_df.dropna()
    
    # merge in tobacco data
    merged_df = merged_df.merge(tobacco_df, how='inner', on='SEQN')

    print('merged_df len:', len(merged_df))
    return merged_df

if __name__ == "__main__":
    df = main()
    df.to_csv('../refined_data/merged_data.tsv', sep='\t')