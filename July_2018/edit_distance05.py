# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:39:24 2017

@author: iar1g09
"""

from __future__ import division
import pandas as pd
import editdistance
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.spatial import distance
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram, fcluster

plt.style.use('ggplot')
sns.set(font_scale = 0.1)
column1 = 'CODEX 4'
por = ' con'
# path of the data file to be analysed
#file_path = "codex_data1.xlsx"
file_path= column1 + "data por" + por + "_sorted.csv"
print(file_path)

# Spatial analysis
spatial = True


# axes labels of the heat map - can be the tituli, can be the amphora's number etc
axes = 'INV'
#'INV', 'CODEX'

# how big do you want the picture. It's in inches so just experiment a bit to get the right shape.
figure_size = (10, 10)
# Must be two numbers with a comma between, (25, 25) works well usually

# do you want the clusters?
clustered = True
# True, False

# do you want the labels on the squares? 
annotate = False
# True, False

#How big do you want the annotation to be
font_size = 6


# Value for the threshold in the dendrogram
# threshold = 20



# True, False

if spatial:
    #Do you want only the first value per amphora to be considered?
    drop_repeats = True
else:
    drop_repeats = False


def read_data(file_path):
    """
    1. read the file with the codex
    2. if we want to analyse only one per codex per amphora use drop_repeats
    """

#    1. read the file with the codex
    
    df = pd.read_csv(file_path)

#    2. if we want to analyse only one per codex per amphora use drop_repeats
    if drop_repeats:
        df = df.groupby('INV').first()   
        # since we have removed some rows the index needs to be reset
        # The drop argument ensures that the old index is not kept  
       
        df = df.reset_index()      

    return df

def analyse_data(list_of_tit):
    """ 1. create a matrix of editdistance values
        2. save to a csv for other sciripts and future generations
    """

    # get the size of the original data
    a, b = list_of_tit.shape

    # this is probably an overkill casting it from lists to data frames but hey it works
    # so here we initiate an empty matrix the size of len(data)xlen(data)   
    matrix = [[ [] for x in range(a)] for x in range(a)]
    
    # record the edit distance for each combination
    for i in range(a):
        for j in range(a):
            temp = editdistance.eval(list_of_tit['CODEX'][i], list_of_tit['CODEX'][j])
            #  version for combining more than one column 
            #  temp = editdistance.eval(list_of_tit[column1][i]+list_of_tit['CODEX'][i], list_of_tit[column1][j]+list_of_tit['CODEX'][j])
            matrix[i][j] = temp
        
    # recast it into a data frame (yeah, I know)   
    matrix = pd.DataFrame(matrix, columns = list_of_tit[axes], index = list_of_tit[axes])

    matrix.to_csv('results/matrix'+ file_path+ str(spatial)+'.csv', encoding = 'utf-8')   
    print('matrix size: ', len(matrix))
    return matrix    


def visualise(matrix, cluster_type, name, pal, col):  
    """ 1. calculate the clusters
        2. prep the side pane (with the independent variable)
        3. create the visualisation
            a. clustermaps
                . annotated
                . not annotated
            c. heatmap (no clustering)
                . annotated
                . not annotated   
                    
    """
    
#   1. calculate the clusters
    row_linkage = hierarchy.linkage(
        distance.pdist(matrix), method='average') # Ferreira and Hitchcock 2009 BUT see below
    
    col_linkage = hierarchy.linkage(
        distance.pdist(matrix.T), method='average') # gives the best Cophenetic Correlation Coefficient of 0.90792
 
#   2. prep the side pane (with the independent variable)
    yticks = matrix.index
    if spatial:
        a = np.sort(cluster_type.unique())
        # remove all non-locations        
        a = a[a!='0'] 
        a = a[a!='00']
        a = a[a!='000'] 
        lut = dict(zip(a, sns.color_palette(pal, len(cluster_type.unique()))))
        
    else:            
        a = cluster_type.unique()
        a = np.roll(a,-3)
        lut = dict(zip(cluster_type.unique(), sns.color_palette(pal, len(cluster_type.unique()))))

    row_colors = cluster_type.map(lut)

    
#   3. create the visualisation
    # create heatmap, format as an integer, make lines between squares, annotate with numbers, make the annotation size 7
    
    title = (file_path[:-4])

    if clustered: 

        if annotate:      
            
            clustergrid = sns.clustermap(matrix.reset_index(drop=True), row_linkage=row_linkage, col_linkage=col_linkage,  method="average", annot = True, annot_kws={"size": font_size}, row_colors=row_colors, figsize=figure_size,linewidth=0.15, yticklabels=yticks)
            plt.setp(clustergrid.ax_heatmap.get_yticklabels(), rotation=0)
            plt.figure(figsize = figure_size)
    
            plt.title('clustermap of the '+ title, fontsize = 20, loc = 'right')
#            a = np.roll(a,-3)
            
            for label in a:
                clustergrid.ax_col_dendrogram.bar(0, 0, color=lut[label], label=label, linewidth=0)
                clustergrid.ax_col_dendrogram.legend(loc="center", ncol=col)
            
            
        else: 
            plt.figure()

            clustergrid = sns.clustermap(matrix.reset_index(drop=True), row_linkage=row_linkage, col_linkage=col_linkage,  method="average", row_colors=row_colors,linewidth=0.15, yticklabels=yticks)
            plt.setp(clustergrid.ax_heatmap.get_yticklabels(), rotation=0)
            plt.title('clustermap of the '+ title, fontsize = 20, loc = 'right')

#            a = cluster_type.unique()
#            a = np.roll(a,-3)
            
            for label in a:
                clustergrid.ax_col_dendrogram.bar(0, 0, color=lut[label], label=label, linewidth=0)
                clustergrid.ax_col_dendrogram.legend(loc="center", ncol=col)
            
    else: 
        if annotate:    
            clustergrid = sns.heatmap(matrix, fmt="d", linewidths=.5, annot=True, annot_kws={"size": font_size}, figsize = figure_size)
            plt.setp(clustergrid.ax_heatmap.get_yticklabels(), rotation=0)
            plt.title('clustermap of the '+ title, fontsize = 20, loc = 'right')

        else:
            clustergrid = sns.heatmap(matrix, fmt="d", linewidths=.5, figsize = figure_size)
            plt.setp(clustergrid.ax_heatmap.get_yticklabels(), rotation=0)
            plt.title('clustermap of the '+ title, fontsize = 20, loc = 'right')

    clustergrid.savefig('results/' + name + file_path[:-4] + '.pdf', format = 'PDF')

    return row_linkage, clustergrid, row_colors, yticks
#    basic visual:
#    plt.pcolor(matrix)
#    plt.yticks(np.arange(0.5, len(matrix.index), 1), matrix.index)  
#    plt.xticks(np.arange(0.5, len(matrix.columns), 1), matrix.columns, rotation = 'vertical')  
#    plt.savefig("matrix.pdf", format = 'PDF')   
    


    
    
def main():

    #_____________ MAIN_________________
    
    # 1. read data 
    df = read_data(file_path)
    
    # 2. record the dataset the analysis will be done on, no further data manipulation 
    df.to_csv('results/dfused_' + file_path, encoding = 'utf-8')
    
    # 3. create a matrix of editdistances
    
#   This line is for testing the fake data 
#    df['CODEX'] = pd.read_csv('fake_data.csv')
    list_of_tit = df[['INV', 'CODEX' ]]
    matrix = analyse_data(list_of_tit)
    
    # 4. use this matrix to generate images - it's the same heatmap but with different side panels
    
    lit = pd.Series(df.LITTERAE)
    con = pd.Series(df.CONCEPTUM)
    reg = pd.Series(df.REGESTUM)
    
    regio = pd.Series(df.locR)
    insula = pd.Series(df.locI)
    aed = pd.Series(df.locA)
    
    if spatial:
        list_col = [regio, insula, aed]
        variables = ['Regio', 'Insula', 'Aedificium']
        palettes = [["#a50026","#d73027","#f46d43","#fdae61","#fee08b","#d9ef8b","#a6d96a","#66bd63","#1a9850","#006837"], 
                    ['#6a5acd','#705dcb','#7560c9','#7a63c6','#8066c3','#8569c1','#896dbe','#8e6fbc','#9272ba','#9676b7','#9a79b5','#9d7cb2','#a180af','#a582ad','#a886aa','#ac89a8','#af8da5','#b28fa3','#b6939f','#b8969d','#bb9a9a','#be9d97','#c1a195','#c4a392','#c7a78f','#c9aa8c','#ccae89','#cfb186','#d1b583','#d4b87f','#d6bb7d','#d9bf79','#dbc276','#ddc672','#e0c96f','#e2cd6a','#e4d167','#e7d463','#e9d85f','#ebdb5a','#eddf56','#efe350','#f1e54c','#f3e946','#f5ed40','#f7f139','#f9f430','#fbf828','#fdfb19','#ffff00'],
                     sns.cubehelix_palette(len(df.locA.unique()), start=.5, rot=-.75)]
   
    else:
        list_col = [lit, con, reg]
        variables = ['lit', 'con', 'reg']
        palettes =[["#b2df8a","#a6cee3","#fdb863"],["#984ea3", "#ff7f00", "#33a02c", "#a65628", "#1f78b4", "#fdbf6f" , "#e31a1c",  "#a6cee3",  "#b2df8a","#999999"],["#984ea3", "#ff7f00", "#33a02c", "#a65628", "#1f78b4", "#fdbf6f" , "#cab2d6",  "#a6cee3",  "#b2df8a","#e31a1c","#999999" ]]

    
    columns = [3, 5, 6]
    for i in range(len(list_col)):
        rl, cg, rc, yt = visualise(matrix, list_col[i], variables[i], palettes[i], columns[i])
'''
# These have been moved to the next file 'data_manipulation2.py'
def analysis(df, rl, yt):
    # 5. Make dendrograms    
    for threshold in range(0, 60, 10):
#        make_dendro(df, rl, cg, yt, threshold)
    
    # 6. Here we do the analysis but there's a separate script for it
    # calculate clusters
        clusters=pd.Series((fcluster(rl, threshold, criterion = 'distance')), index = yt)
    
        df_final = pd.merge(df,  clusters.to_frame('cluster'), left_on = 'INV', right_index=True)
        df_final.to_csv('output_df' + str(threshold) + file_path[:-4] + '.csv')
        
    cluster_list = ['REGESTUM', 'LITTERAE', 'CONCEPTUM', 'locR', 'locI', 'locA']
    output = []
    import scipy.stats as stats
    
    for i in cluster_list:
        ct1 = pd.crosstab(df_final.cluster, df_final[i])
        cs1 = stats.chi2_contingency(ct1)
        print('Outcome '+ i )
        print (cs1[:3])
        output.append(cs1)
        
def make_dendro(df, row_linkage, clustergrid, yticks, threshold):
    """
    Make a dendrogram showing the clustering
    """
    
    plt.figure(figsize = figure_size)
    title = (file_path[:-4])
    plt.title('dendrogram of the '+ title, fontsize = 20)
    
    dendrogram(row_linkage,  leaf_rotation = 90, color_threshold=threshold, leaf_font_size = 10, labels = yticks)  #labels = df.index[clustergrid.dendrogram_row.reordered_ind])
    
    plt.savefig('results/dendrogram' + file_path[:-4] + '.pdf', format = 'PDF')
    plt.show()
 '''   

main()