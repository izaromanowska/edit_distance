# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:18:14 2017

@author: iromanow
"""
from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram, fcluster
import seaborn as sns
plt.style.use('ggplot') 

column1 = 'CODEX 6'
por = ' con_lit'
file_path= column1 + "data por" + por + "_sorted.csv"

spatial = False

#True, False
sns.set(font_scale = 1.5)

def calculations(matrix):
    """ First calculate the clusters
        Then flatten them using the threshold supplied
    """
    yticks = matrix.index
    print(len(matrix))
#    1. Calculating clutsers, the average method gives the best Cophenetic Correlation Coefficient of 0.90792
    row_linkage = hierarchy.linkage(
        distance.pdist(matrix), method='average')
    
#   2. Flatten the clusters on a given threshold    
    clusters=pd.Series((fcluster(row_linkage, threshold, criterion = 'distance')), index = yticks)
    print(len(clusters))
    return row_linkage, yticks, clusters

def make_dendro( row_linkage, yticks, i):
    """
    Create the dendrograms, threshold is supplied from globals
    """
    
    title = (file_path[:-4])
    plt.figure(figsize = (50,20))
    plt.title('dendrogram of the '+ title + ' Threshold: ' + str(i), fontsize = 20)
    dendrogram(row_linkage,  leaf_rotation = 90, color_threshold=threshold, leaf_font_size = 7.0, labels = yticks)  #labels = df.index[clustergrid.dendrogram_row.reordered_ind])
    plt.ylim(0, 500)
    plt.savefig('results/dendrogram' + file_path[:-4] + str(i) +'.pdf', format = 'PDF')
    plt.show()

def do_chi2(df):
    """
    Do stats: 
        
    """
    
#    print(df_final)
    if spatial:
        cluster_list = ['locR', 'locI', 'locA']       
    else:
        cluster_list = ['REGESTUM', 'LITTERAE', 'CONCEPTUM']

    output = []
    import scipy.stats as stats
    for i in cluster_list:
        
        ct1 = pd.crosstab(df_final.cluster, df_final[i])
        cs1 = stats.chi2_contingency(ct1)
#        print('Outcome '+ i )
#        print (cs1)
        cs1 = (i, ) + cs1
        cs1 = (threshold,)+cs1
        output.append(cs1)
    print (threshold)
    return output

all_outputs = [] 
#df = pd.read_csv('results/dfused_' + file_path)
df = pd.read_csv(file_path)
if spatial:
    df = df.groupby('INV').first().reset_index()
    print(df.head())
print(len(df))
if spatial:    
    matrix = pd.read_csv('results/matrix' + file_path + 'True.csv', index_col = 0)
else: 
    matrix = pd.read_csv('results/matrix' + file_path + 'False.csv', index_col = 0)

print('matrix length: ', len(matrix))
for i in range (10, 100, 10):
    threshold = i
    print (i)
    rl, yt, clu = calculations(matrix)
    if spatial == True:
        make_dendro(rl, yt, i)
    clu = clu.reset_index(drop = False)
    clu.columns = ['INV', 'cluster']

    #df_final = pd.merge(df,  clu, right_index = True, left_index = True)
    df_final = pd.merge(df,  clu, left_on = 'INV', right_on = 'INV')

#    df_final = pd.merge(df,  clu.to_frame('cluster'), left_on = 'INV', right_index=True)

#    df_final = pd.merge(df,  clu.to_frame('cluster'), left_on = 'INV', right_index = True)
#    print (df_final.cluster)
#    df[ 'threshold' + str(i)] = clu.to_frame('cluster')
    df[ 'threshold' + str(i)] = df_final.cluster
    
    
    output = do_chi2(df_final)
    
    all_outputs.extend(output)

if spatial:
    df.to_csv('results/output_df' + str(threshold) + file_path[:-4] + '.csv', encoding = 'utf-8')
    
results = pd.DataFrame(all_outputs, columns = ['threshold','type','stats', 'p', 'dof', 'array'])
    
#results.groupby('type').plot(x = 'threshold', y = 'p', subplots = True, legend = True, title = results.type)

for title, group in results.groupby('type'):
    group.plot(x='threshold', y='p', title = title) 
    plt.savefig('results/p' + file_path[:-4] + str(title) +'.pdf', format = 'PDF')



    