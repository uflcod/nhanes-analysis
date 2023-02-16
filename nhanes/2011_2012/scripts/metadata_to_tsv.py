#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creates TSVs of all the variable names, descriptions, and values.
Files produced:
  - metadata_vars.tsv: contains the data variable names and descriptions
  - metadata_values.tsv: contains the value sets and description for each variable
  - metadata.tsv: merges of the metadata_vars.tsv and metadata_values.tsv files
"""

import os
import pandas as pds
from glob import glob

def main():
    path = os.getcwd()
    tsv_files = glob(os.path.join(path, "../metadata/*_meta.tsv"))
    
    tsvs = [pds.read_table(f) for f in tsv_files]
    var_df = pds.concat(tsvs)
    var_df.to_csv('../metadata/metadata_vars.tsv', sep='\t', index=False)

    # temp_df = var_df.head() # testing
    # print(temp_df)
    value_dfs = []
    for var_name in var_df['Variable.Name'].values:
        fname = f'../metadata/metadata_values/{var_name}.tsv'
        if os.path.exists(fname):
            value_dfs.append(pds.read_table(fname))
            value_dfs[-1]['Variable.Name'] = var_name

    value_df = pds.concat(value_dfs)
    value_df.to_csv('../metadata/metadata_values.tsv', sep='\t', index=False)

    # merge metadata vars with values
    df = var_df.merge(value_df, how='left', on='Variable.Name')
    df = df.drop_duplicates()

    df.to_csv('../metadata/', sep='\t', index=False)
metadata.tsv
if __name__ == "__main__":
    main()