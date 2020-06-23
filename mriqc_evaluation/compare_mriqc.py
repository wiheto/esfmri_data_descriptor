import pandas as pd
import json
import bids
import matplotlib.pyplot as plt
import plotje

# Download data from here: Esteban, O. et al. Crowdsourced MRI quality metrics
# and expert quality annotations for training of humans and machines. Sci Data 6, 30 (2019).
# Then run make_distributions.py to summarize the data from this snapshot
summary_path = './data/summary/bold_curated'
dataset = '/home/william/datasets/es-fmri_v2/'
dfd = pd.read_csv(summary_path + qc + '_summary.csv', index_col=[0])


layout = bids.BIDSLayout(dataset)
layout.add_derivatives(dataset + '/derivatives/')
layout = layout.to_df()

keeprow = []
for i, n in layout.iterrows():
    if 'mriqc_output' in n['path'] and n['path'].endswith('.json'):
        keeprow.append(i)

layout = layout.loc[keeprow]
layout_bold = layout[layout['suffix'] == 'bold']

params = [('pre', 'rest', 'preop'),
        ('es', 'es', 'postop')]

qcmet = {}
qcdesc = {}
for p in params: 
    qcmet[p[0]] = {} 
    qcdesc[p[0]] = {} 
    for n,_ in dfd.iteritems(): 
        qcmet[p[0]][n] = []

    layout_tmp = layout[layout['task'] == p[1]]
    layout_tmp = layout_tmp[layout_tmp['session'] == p[2]]

    for _, f in layout_tmp.iterrows(): 
        with open(f['path']) as json_data:
            d = json.load(json_data)

        for n,_ in dfd.iteritems(): 
            qcmet[p[0]][n].append(d[n])

    for n,_ in dfd.iteritems(): 
        qcdesc[p[0]][n] = pd.Series(qcmet[p[0]][n]).describe()


fig, ax = plt.subplots(13, 1, figsize=(5,15))
ax = ax.flatten()

qoi = ['aor','aqi','dvars_std','dvars_vstd','efc','fber','fd_mean','gcor','gsr_x','gsr_y','snr','tsnr']
dfd_chosen = dfd[qoi]

for i, n in enumerate(dfd_chosen.iteritems()): 
    a = n[0]
    ax[i].plot([dfd[a]['mean']-dfd[a]['std'], dfd[a]['mean']+dfd[a]['std']], [2,2], color='cornflowerblue')
    ax[i].plot([qcdesc['pre'][a]['mean']-qcdesc['pre'][a]['std'], qcdesc['pre'][a]['mean']+qcdesc['pre'][a]['std']], [1,1], color='salmon')
    ax[i].plot([qcdesc['es'][a]['mean']-qcdesc['es'][a]['std'], qcdesc['es'][a]['mean']+qcdesc['es'][a]['std']], [0,0], color='plum')

    ax[i].scatter(dfd[a]['mean'], [2], marker='s', color='cornflowerblue')
    ax[i].scatter(qcdesc['pre'][a]['mean'], [1], marker='s', color='salmon')
    ax[i].scatter(qcdesc['es'][a]['mean'], [0], marker='s', color='plum')

    ax[i].scatter(dfd[a]['25%'], [2], marker='|', color='cornflowerblue')
    ax[i].scatter(qcdesc['pre'][a]['25%'], [1], marker='|', color='salmon')
    ax[i].scatter(qcdesc['es'][a]['25%'], [0], marker='|', color='plum')

    ax[i].scatter(dfd[a]['75%'], [2], marker='|', color='cornflowerblue')
    ax[i].scatter(qcdesc['pre'][a]['75%'], [1], marker='|', color='salmon')
    ax[i].scatter(qcdesc['es'][a]['75%'], [0], marker='|', color='plum')

    ax[i].scatter(dfd[a]['50%'], [2], marker='d', color='cornflowerblue')
    ax[i].scatter(qcdesc['pre'][a]['50%'], [1], marker='d', color='salmon')
    ax[i].scatter(qcdesc['es'][a]['50%'], [0], marker='d', color='plum')



    if ax[i].get_xlim()[0]<0 and dfd[a]['min']>=0 and qcdesc['pre'][a]['min'] >= 0 and qcdesc['es'][a]['min'] >= 0:
        ax[i].set_xlim([0, ax[i].get_xlim()[1]])

    if a == 'dvars_vstd':
        ax[i].set_xlim([0.75, 1.5])
        ax[i].scatter([1.5],[2], marker=5, color='cornflowerblue')
        ax[i].scatter([0.75],[2], marker=4, color='cornflowerblue') 


    elif a == 'fber':
        ax[i].set_xlim([0, 25000])
        ax[i].scatter([25000],[2], marker=5, color='cornflowerblue') 

    elif a == 'fd_mean':
        ax[i].set_xlim([0, 1.5])
        ax[i].scatter([1.5],[2], marker=5, color='cornflowerblue') 

    elif a == 'gsr_x':
        ax[i].set_xlim([-0.05, 0.05])
        ax[i].scatter([0.05],[2], marker=5, color='cornflowerblue')
        ax[i].scatter([-0.05],[2], marker=4, color='cornflowerblue') 

    elif a == 'gsr_y':
        ax[i].set_xlim([0.01, 0.06])
        ax[i].scatter([0.06],[2], marker=5, color='cornflowerblue')
        ax[i].scatter([0.01],[2], marker=4, color='cornflowerblue') 

    plotje.styler(ax[i], leftaxis='off', ylabel=a)

plt.tight_layout()

fig.savefig('/home/william/work/esfmri/howsmyqc.svg')