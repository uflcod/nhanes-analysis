#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pds
import numpy as np
from sklearn.preprocessing import StandardScaler

def main(cfq_file='../data/CFQ_G_cognitive_functioning.tsv') -> pds.DataFrame:
    # load cognitive functioning questionnaire
    cfq_df = pds.read_table(cfq_file, index_col='SEQN')
    print('cfq_df len:', len(cfq_df))

    # filter for patients that completed all 4 of the CERAD tests (CFDCCS)
    # for reference
    # 1: Four completed recalls (count: 1451)
    # 2: One to three completed recalls (count: 17)
    # 3: Not done (count: 42)
    # 4: Missing (count: 177)
    cfq_df = cfq_df.query("CFDCCS == 1")
    print('cfq_df completed all 4 of the CERAD len:', len(cfq_df))

    # filter for patients completed the Animal Fluency: Sample Practice Pretest (CFDAPP)
    # for reference
    # Code  Value       Count
    # 1 	Passed 	    1449
    # 2 	Failed 	    7 	
    # 3 	Not done 	54 	
    # . 	Missing 	177 
    cfq_df = cfq_df.query("CFDAPP == 1")
    print('cfq_df completed Animal Fluency len:', len(cfq_df))

    ## filter for patients that completed the Digit Symbol: Sample Practice Pretest (CFDDPP)  
    # for reference  
    # Code    Description 	Count 	  
    # 1       Passed 	        1422 	  
    # 2 	  Failed 	        52 	  
    # 3 	  Not done 	    36 	  
    # . 	  Missing 	    177  
    cfq_df = cfq_df.query("CFDDPP == 1")
    print('cfq_df completed Digit Symbol len:', len(cfq_df))

    # create subset of scores
    # CFDCSR - CERAD: Score Delayed Recall
    # CFDCIR - CERAD: Intrusion word count Recall
    # CFDAST - Animal Fluency: Score Total
    # CFDDS - Digit Symbol: Score
    score_df = cfq_df[['CFDCSR', 'CFDCIR', 'CFDAST', 'CFDDS']]

    # standardize scores with sklearn StandardScaler
    # (other normalization methods can be explored too)
    std_scaler = StandardScaler()
    zscore_df = pds.DataFrame(std_scaler.fit_transform(score_df), columns=score_df.columns, index=score_df.index)

    # rename z-score column names
    zscore_name_map = {'CFDCSR': 'z_CFDCSR', 'CFDCIR': 'z_CFDCIR', 'CFDAST': 'z_CFDAST', 'CFDDS': 'z_CFDDS'}
    zscore_df = zscore_df.rename(columns=zscore_name_map)
    print('zscore len', len(zscore_df))

    # return merge of score and zscore dfs
    return pds.merge(score_df, zscore_df, how='inner', on='SEQN')

if __name__ == "__main__":
    df = main()
    df.to_csv('../refined_data/cognitive_scores.tsv', sep='\t')