#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pds

def main(demo_file='../data/DEMO_G_demographics.tsv') -> pds.DataFrame:
    demo_df = pds.read_table(demo_file, index_col='SEQN')

    # subset columns
    # RIDAGEYR: Age in years of the participant at the time of screening
    # RIAGENDR: Gender of the participant.
    # code reference
    #    1: Male
    #    2: Female
    #    .: Missing
    # RIDRETH1: Recode of reported race and Hispanic origin information
    # code reference
    #    1: Mexican American
    #    2: Other Hispanic
    #    3: Non-Hispanic White
    #    4: Non-Hispanic Black
    #    5: Other Race - Including Multi-Racial
    #    .: Missing
    # RIDRETH3: Recode of reported race and Hispanic origin information, with Non-Hispanic Asian Categor
    # code reference
    #    1: Mexican American
    #    2: Other Hispanic
    #    3: Non-Hispanic White
    #    4: Non-Hispanic Black
    #    6: Non-Hispanic Asian
    #    7: Other Race - Including Multi-Racial
    #    .: Missing
    # DMDMARTL: Marital status
    # code reference
    #    1: Married
    #    2: Widowed
    #    3: Divorced
    #    4: Separated
    #    5: Never married
    #    6: Living with partner
    #    77: Refused
    #    99: Don't Know
    #    . : Missing
    # 
    # WTINT2YR: Full sample 2 year interview weight
    # WTMEC2YR - Full sample 2 year MEC exam weight
    demo_df = demo_df[['RIDAGEYR', 'RIAGENDR', 'RIDRETH1', 'RIDRETH3', 'DMDMARTL', 'WTINT2YR', 'WTMEC2YR']]
    print('demo_df len', len(demo_df))

    return demo_df

if __name__ == "__main__":
    df = main()
    df.to_csv('../refined_data/demographics.tsv', sep='\t')