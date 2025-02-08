#%%
import pandas as pds
import numpy as np
from itertools import groupby

#%%
# load dentition data
dent_df = pds.read_table('../data/OHXDEN_G_dentition.tsv', index_col='SEQN')

#%%
# load perio data
perio_df = pds.read_table('../data/OHXPER_G_perio.tsv', index_col='SEQN')

#%%
# subset data for complete (i.e., "1") dentition and perio status
dent_df = dent_df[dent_df.OHDDESTS == 1]
perio_df = perio_df[perio_df.OHDPDSTS == 1]
print(f'dent_df: {len(dent_df)}, perio_df: {len(perio_df)}')
# dent_df: 8439, perio_df: 3685

#%%
# drop wisdom teeth (1, 16, 17, 32) cols, these are not used in the perio exam
dent_df= dent_df.drop(['OHX01TC', 'OHX16TC', 'OHX17TC', 'OHX32TC'], axis=1)

#%%
# subset to tooth columns(i.e., ignore coronal caries cols)
tooth_cols = [        
    c for c in dent_df.columns 
    if c.endswith("TC") and not c.endswith("CTC")
]
dent_df = dent_df[tooth_cols]
len(dent_df) # 8439

#%%
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
len(dent_df) # 8439

#%%
# replace 2 (permenant tooth) with 1 (so 1: present, 0: missing)
# this makes it easy to sum up the tooth number of teeth
dent_df = dent_df.replace(2, 1)
len(dent_df) # 8439

#%%
# calc number of teeth for patient
dent_df['num_teeth'] = dent_df[tooth_cols].sum(axis=1)
len(dent_df) # 8439

#%%
# drop rows for patients w/o teeth (i.e., num_teeth == 0)
dent_df = dent_df[dent_df['num_teeth'] > 0] 
len(dent_df) # 6999

#%%
# test that only values 0 and 1 are used in the tooth columns
np.unique(dent_df[tooth_cols].values.ravel()) # [0, 1]

#%%
# in dent_df replace tooth 'OHX' with 'tooth_' and replace TC with ""
tooth_map = {
    c: c.replace("TC", "").replace("OHX", "tooth_") for c in tooth_cols
}
# dent_df.rename(columns=tooth_map)
# ---------------------

#%%
# only include perio exams for patients that have teeth
intersect = np.intersect1d(perio_df.index.values, dent_df.index.values)
perio_df = perio_df.loc[intersect,:]
len(perio_df) # 3321

#%%
# in perio_df find columns that calculate CAL
# i.e., LA: Calculation of : (FGM to CEJ measurement) - (FGM to sulcus base measurement) (mm)
cal_cols = [
    c for c in perio_df.columns if c.endswith('LA', 5, 7)
]
perio_df = perio_df[cal_cols]
len(perio_df) # 3321

#%%
# replace missing vals with nan
# note: 99 means 'cannot be assessed'
perio_df[cal_cols] = perio_df[cal_cols].replace(['.', 99], np.nan)
len(perio_df) # 3321

#%%
# exclude CAL measurements performed on primary teeth or implants
# primaries and implants will have a '0' in the associated dentition column
# to associate CAL with tooth, create a map for each tooth CAL group
# note: groups are based on the first 5 chars in CAL column name (e.g., OHX02)
tooth_cal_map = {
    f'{k}TC':list(g) for k, g in groupby(cal_cols, key=lambda col: col[:5])
}

#%%
# k holds the name of the tooth column (e.g., OHX02TC)
# v holds the perio CAL columns for the tooth
# since (from above) every index in peiro_df is in dent_df
# check if the tooth has been counted in dent_df
# if it has not been count (i.e., equals 0) set CAL columns to NAN
for k, v in tooth_cal_map.items():
    for idx in perio_df.index:
        if dent_df.loc[idx, k] == 0:
            perio_df.loc[idx, v] == np.nan
len(perio_df) # 3321

#%%
{c[:5] for c in perio_df.columns}

#%%
# for each perio CAL find max depth
perio_df['max_CAL'] = perio_df[cal_cols].max(axis=1)
len(perio_df) # 3321

#%%
# drop rows for patients w/o perio info
perio_df = perio_df[perio_df['max_CAL'].notnull()]
len(perio_df) # 3309


#%%
perio_df.loc[62177, 'max_CAL']
# perio_df.loc[63, cal_cols]
# perio_df.max_CAL.unique()

#%%
vals = perio_df.loc[62177, cal_cols].values
vals

#%%
vals[vals == 4]
len(vals[vals >= 4])

#%%
def calc_CAL_gt(vals):
    """calculates the numer of CAL measurements >= 4, 5, 6, 7 mm"""
    num_gt_3 = num_gt_4 = num_gt_5 = num_gt_6 = 0
    
    num_gt_3 = len(vals[vals > 3])
    num_gt_4 = len(vals[vals > 4])
    num_gt_5 = len(vals[vals > 5])
    num_gt_6 = len(vals[vals > 6])
    
    return num_gt_3, num_gt_4, num_gt_5, num_gt_6

#%%
# calc CAL measurement thresholds
for idx in perio_df.index:
    vals  = perio_df.loc[idx, perio_cols].values
    num_gt_3, num_gt_4, num_gt_5, num_gt_6 = calc_CAL_gt(vals)
    
    perio_df.loc[idx, 'num_teeth_gt_3'] = num_gt_3
    perio_df.loc[idx, 'num_teeth_gt_4'] = num_gt_4
    perio_df.loc[idx, 'num_teeth_gt_5'] = num_gt_5
    perio_df.loc[idx, 'num_teeth_gt_6'] = num_gt_6

#%%
for k, g in groupby(cal_cols, key=lambda col: col[:5]):
    cal_name = f'max_{k}_CAL'
    cal_names = list(g)
    
    # print(col_name)
    # print(col_names)
    perio_df[cal_name] = perio_df[cal_names].max(axis=1)
    
#%%
max_names = ['SEQN'] + [c for c in perio_df.columns if c.startswith('max_')]
max_df = perio_df[max_names]

#%%
# for each tooth find the max CAL for that tooth
# k holds the name of the tooth column (e.g., OHX02TC)
# v holds the perio CAL columns for the tooth
for k, v in tooth_cal_map.items():
    max_cal_name = f'max_{k}_CAL'
    for idx in perio_df.index:
        perio_df.loc[idx, max_cal_name] = perio_df.loc[idx, v].max()

#%%
merged_df = pds.merge(perio_df, dent_df, how='inner', on='SEQN')
len(merged_df)
    
    
                 





