# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 16:10:38 2018

@author: iromanow
"""

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

codex = 'CODEX 4'
por = ' con'

df = pd.read_csv('results/merged_df90'+codex+'data por'+por+'_sorted.csv')
sns.set(font_scale = 1.8)
plt.figure(figsize = (25,25))
#sns.countplot(x ='INV', data = data)
drop_repeats = True
if drop_repeats:
    df = df.groupby('INV_x').first()   
for i in range(9):
    plt.subplot(3,3,i+1)
    col = 'threshold' + str((i+1)*10)
    sns.countplot(x = col, order = df[col].value_counts().index, data = df)
    if i < 2:
        plt.xticks(fontsize = 9, rotation = 90)
    else:
        plt.xticks(rotation = 90)
    plt.tight_layout()
    
    
plt.savefig('results/thresholdsVSclusters.png')
  
no_clusters = []
labels = []
for i in range(9):
    col = 'threshold' + str((i+1)*10)  
    no_clusters.append(df[col].nunique())
    labels.append(col)

plt.figure()
plt.plot(no_clusters)
plt.xticks(np.arange(len(labels)), labels, rotation = 90)
plt.ylabel('Number of clusters')
plt.savefig('results/NoClusters.png')