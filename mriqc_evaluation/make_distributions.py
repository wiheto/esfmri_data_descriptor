
import pandas as pd 
import numpy as np 
snapshot_path = './data/mriqc_snapshot/'
summary_path = './data/summary/'
bins = 1000

files = ['bold_curated', 'T1w_curated', 'T2w_curated']

for f in files: 
    df = pd.read_csv(snapshot_path + f + '.csv')
    df = df.replace([np.inf, -np.inf], np.nan)
    dfd = df.describe() 
    cols = list(dfd.columns)
    cols = [c for c in cols if not c.startswith('bids_meta') and not c.startswith('metadata_') and c != 'provenance.settings.fd_thres' and c != 'null_count']
    dfd = dfd[cols]
    df = df[cols]
    dfd.to_csv(summary_path + f + '_summary.csv')
    for i,c in df.iteritems(): 
        c = c.replace([np.inf, -np.inf], np.nan)
        c = c.dropna()
        histcut = pd.cut(c, bins, duplicates='drop', precision=5).value_counts().sort_index()
        histcut.to_csv(summary_path + f + '_' + i + '_hist.csv')