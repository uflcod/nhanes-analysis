#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pds
import numpy as np
from itertools import groupby


def calc_CAL_gt(vals):
    """calculates the numer of CAL measurements > 3, 4, 5, 6 mm"""
    num_gt_3 = num_gt_4 = num_gt_5 = num_gt_6 = 0
    
    num_gt_3 = len(vals[vals > 3])
    num_gt_4 = len(vals[vals > 4])
    num_gt_5 = len(vals[vals > 5])
    num_gt_6 = len(vals[vals > 6])

    return num_gt_3, num_gt_4, num_gt_5, num_gt_6


def make_dentition_df(dentition_file:str)-> pds.DataFrame:
    dent_df = pds.read_table(dentition_file, index_col='SEQN')

    # subset for "complete" dentition
    dent_df = dent_df[dent_df.OHDDESTS == 1]

    # drop wisdom teeth (1, 16, 17, 32) cols, these are not used in the perio exam
    dent_df= dent_df.drop(['OHX01TC', 'OHX16TC', 'OHX17TC', 'OHX32TC'], axis=1)

    # subset to tooth columns(i.e., ignore coronal caries cols)
    tooth_cols = [        
        c for c in dent_df.columns 
        if c.endswith("TC") and not c.endswith("CTC")
    ]
    dent_df = dent_df[tooth_cols]

    # keep only permanent teeth
    # for reference: 
    #    1 - primary, 2 - permanent, 3 - implant, 4 - 	tooth not present
    #    5 - Permanent dental root fragment present, 9 - Could not assess
    #    '.' - missing
    dent_df = (
        dent_df
        .replace(['.', 1, 3, 4, 5, 9], np.nan)
        .fillna(0)
    )

    # replace 2 (permenant tooth) with 1 (so 1: present, 0: missing)
    # this makes it easy to sum up the tooth number of teeth
    dent_df = dent_df.replace(2, 1)

    # calc number of teeth for patient
    dent_df['num_teeth'] = dent_df[tooth_cols].sum(axis=1)

    # drop rows for patients w/o teeth (i.e., num_teeth == 0)
    dent_df = dent_df[dent_df['num_teeth'] > 0] 

    return dent_df

def make_perio_df(perio_file:str, dent_df:pds.DataFrame) -> pds.DataFrame:
    perio_df = pds.read_table(perio_file, index_col='SEQN')

    # subset for "complete" perio
    perio_df = perio_df[perio_df.OHDPDSTS == 1]

    # only include perio exams for patients that have teeth
    intersect = np.intersect1d(perio_df.index.values, dent_df.index.values)
    perio_df = perio_df.loc[intersect,:]

    # in perio_df find columns that calculate CAL
    # i.e.,  has LA in the column name
    # Calculation of: (FGM to CEJ measurement) - (FGM to sulcus base measurement) (mm)
    cal_cols = [
        c for c in perio_df.columns if c.endswith('LA', 5, 7)
    ]
    perio_df = perio_df[cal_cols]

    # replace missing vals with nan
    # note: 99 means 'cannot be assessed'
    perio_df[cal_cols] = perio_df[cal_cols].replace(['.', 99], np.nan)

    # exclude CAL measurements performed on primary teeth or implants
    # primaries and implants will have a '0' in the associated dentition column
    # to associate CAL with tooth, create a map for each tooth CAL group
    # note: groups are based on the first 5 chars in CAL column name (e.g., OHX02)
    tooth_cal_map = {
        f'{k}TC':list(g) for k, g in groupby(cal_cols, key=lambda col: col[:5])
    }

    # k holds the name of the tooth column (e.g., OHX02TC)
    # v holds the perio CAL columns for the tooth
    # since (from above) every index in peiro_df is in dent_df
    # check if the tooth has been counted in dent_df (i.e, > 0)
    # if it has not been counted (i.e., == 0) set CAL columns to NAN
    for k, v in tooth_cal_map.items():
        for idx in perio_df.index:
            if dent_df.loc[idx, k] == 0:
                perio_df.loc[idx, v] == np.nan

    # for each tooth find the max CAL for that tooth
    # k holds the name of the tooth column (e.g., OHX02TC)
    # v holds the perio CAL columns for the tooth
    for k, v in tooth_cal_map.items():
        max_tooth_cal_name = f'max_{k}_CAL' # e.g., max_OHX02TC_CAL
        for idx in perio_df.index:
            perio_df.loc[idx, max_tooth_cal_name] = perio_df.loc[idx, v].max()

    # fetch the max_tooth_cal_names
    max_tooth_cal_names = [
        c for c in perio_df.columns
        if c.startswith('max_OHX')
    ]
    # print(max_tooth_cal_names)
    # calc max CAL for each tooth
    perio_df['max_CAL'] = perio_df[max_tooth_cal_names].max(axis=1)

    # drop rows for patients w/o perio info
    perio_df = perio_df[perio_df['max_CAL'].notnull()]

    # add summary data about CAL ranges
    for idx in perio_df.index:
        vals  = perio_df.loc[idx, max_tooth_cal_names].values
        num_gt_3, num_gt_4, num_gt_5, num_gt_6 = calc_CAL_gt(vals)
        
        perio_df.loc[idx, 'num_teeth_gt_3'] = num_gt_3
        perio_df.loc[idx, 'num_teeth_gt_4'] = num_gt_4
        perio_df.loc[idx, 'num_teeth_gt_5'] = num_gt_5
        perio_df.loc[idx, 'num_teeth_gt_6'] = num_gt_6
    
    return perio_df[['max_CAL', 'num_teeth_gt_3', 'num_teeth_gt_4', 'num_teeth_gt_5', 'num_teeth_gt_6']]

def main(dentition_file='../data/OHXDEN_G_dentition.tsv', 
         perio_file='../data/OHXPER_G_perio.tsv') -> pds.DataFrame:
    
    # load dentition and perio data
    dent_df = make_dentition_df(dentition_file)
    perio_df = make_perio_df(perio_file, dent_df)

    print('*****\n', f'dent_df len: {len(dent_df)}, perio_df len: {len(perio_df)}')

    # merge dentition and perio data
    merged_df = pds.merge(dent_df[['num_teeth']], perio_df, how='inner', on='SEQN')
    print('\n***** merged df\n', merged_df.head())
    print('\n*****\n', f'merged_df len: {len(merged_df)}')

    return merged_df

if __name__ == "__main__":
    df = main()
    df.to_csv('../data/perio_summary.tsv', sep='\t')