import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nib
import seaborn as sns

# fmriprep data path
bids_dir = '/home/william/sherlock/scratch/data/esfmri/derivatives/fmriprep-1.5.1/fmriprep/'
# Where the data is saved
save_path = '/home/william/work/esfmri/figures/fd/'
# Default directory where the raw data is for events file
event_path = '/home/william/sherlock/scratch/data/esfmri/'

subs = [s for s in os.listdir(bids_dir) if s.startswith('sub') and not s.endswith('.html')]

##
## FD Plots for stim on vs stim off postop
##
additional_vals = 1

g_df= []
width = 0.4
si = 0
fig,ax = plt.subplots(1)
subs = sorted(subs)
for s in subs:
    runs = list(set([f.split('run-')[1].split('_')[0] for f in os.listdir(bids_dir + s + '/ses-postop/func/')]))
    for run in runs:
        confpath = bids_dir + s + '/ses-postop/func/'
        event_path_tmp = event_path + s + '/ses-postop/func/'

        # Check bids as missing runs could be inheriting same events as previous files
        if os.path.exists(event_path_tmp + s + '_ses-postop_task-es_run-' + run + '_events.tsv'):
            print('doing this')
            confounds = pd.read_csv(confpath + s + '_ses-postop_task-es_run-' + run + '_desc-confounds_regressors.tsv',sep='\t')
            ev = pd.read_csv(event_path_tmp + s + '_ses-postop_task-es_run-' + run + '_events.tsv',sep='\t')

            img = nib.load(confpath + s + '_ses-postop_task-es_run-' + run + '_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz')
            tr = img.header.get_zooms()[-1]
            time_points = img.shape[-1]
            ev['onset_tr'] = np.round(ev['onset']/tr)
            evvals = []
            for n in range(additional_vals+1):
                evvals.append(ev['onset_tr'].values+n)
            evvals = np.concatenate(evvals)
            evvals = np.unique(evvals)
            evvals = evvals[evvals<time_points]

            nonevvals = np.arange(time_points)
            nonevvals = np.array(list(set(nonevvals).difference(evvals)))

            df = pd.DataFrame()
            df['fd'] = confounds['framewise_displacement'].values
            df['gs'] = confounds['global_signal'].values - np.mean(confounds['global_signal'].values)
            df['stim'] = 0
            df['stim'][evvals] = 'es-on'
            df['stim'][nonevvals] = 'es-off'
            df['sub'] = s
            df['run'] = run
            g_df.append(df)

df = pd.concat(g_df)
df.reset_index(inplace=True)

sns.set(style="whitegrid", palette="muted", color_codes=True)

# Plot dual violin plot for each comparison
fig,ax = plt.subplots(1,figsize=(12,4))
sns.violinplot(x="sub", y="fd", hue="stim",
    split=True, inner="quart",
    data=df,ax=ax,alpha=.5)
sns.despine(left=True)
#ax.set_yscale('log')
ax.set_xticklabels(subs, fontname='Montserrat', fontweight='regular',color='gray')
ax.set_ylim(0,2.5)
ax.set_yticks([0, 1, 2])
ax.set_yticklabels(ax.get_yticks(), fontname='Montserrat', fontweight='regular',color='gray')

ax.set_ylabel('Framewise Displacement', fontname='Montserrat', fontweight='regular',color='gray')
ax.set_xlabel('')

fig.savefig(save_path + 'fd_stimon_vs_stimoff.svg')
fig.savefig(save_path + 'fd_stimon_vs_stimoff.png',r=300)


##
## Global signal plots for stim on vs stim off postop
##

# Also do global signal
# ig,ax = plt.subplots(1,figsize=(12,4))

fig,ax = plt.subplots(1,figsize=(12,4))
sns.violinplot(x="sub", y="gs", hue="stim",
    split=True, inner="quart",
    data=df,ax=ax)
sns.despine(left=True)
ax.set_xticklabels(subs, fontname='Montserrat', fontweight='regular',color='gray')
ax.set_ylabel('Global Signal', fontname='Montserrat', fontweight='regular',color='gray')
ax.set_xlabel('')
ax.set_ylim([-20,10])
ax.set_yticks([-20, -10, 0, 10])
ax.set_yticklabels(ax.get_yticks(), fontname='Montserrat', fontweight='regular',color='gray')

fig.savefig(save_path + 'gs_stimon_vs_stimoff.svg')
fig.savefig(save_path + 'gs_stimon_vs_stimoff.png',r=300)
