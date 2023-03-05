#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pds

def main(tobacco_file='../data/SMQRTU_G_smoking-recent_tobacco_use.tsv') -> pds.DataFrame:
    tobacco_df = pds.read_table(tobacco_file, index_col='SEQN')

    # subset columns
    # SMQ680: Used tobacco/nicotine last 5 days?
    # code reference
    #   1: Yes
    #   2: No
    #   7: Refused
    #   9: Don't know
    #   .: Missing

    # SMQ690A: Used last 5 days - Cigarettes
    # code reference
    #   1: Cigarettes
    #   77: Refused
    #   99: Don't know
    #   .: Missing

    # SMQ690B: Used last 5 days - Pipes
    # code reference
    #   2: Pipes
    #   .: Missing

    # SMQ690C: Used last 5 days - Cigars
    # code reference
    #   3: Cigars
    #   .: Missing

    # SMQ690D: Used last 5 days - Chewing tobacco
    # code reference
    #   4: Chewing tobacco
    #   .: Missing

    # SMQ690E: Used last 5 days - Snuff
    # code reference
    #   5: Snuff
    #   .: Missing

    # SMQ690F: Used last 5 days - Patch, gum, other
    # code reference
    #   6: Nicotine patches, gum, or other nicotine product
    #   .: Missing

    tobacco_df = tobacco_df[['SMQ680', 'SMQ690A', 'SMQ690B', 'SMQ690C', 'SMQ690D', 'SMQ690E', 'SMQ690F']]
    print('tobacco_df len', len(tobacco_df))

    return tobacco_df

if __name__ == "__main__":
    df = main()
    df.to_csv('../refined_data/tobacco.tsv', sep='\t')