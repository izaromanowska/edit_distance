# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 11:45:12 2017

@author: iromanow
"""

import pandas as pd

codex = 'CODEX 4'
por = ' con_lit'


# Remember to move the output file from results to codex 4
#file_path2 = "results/"+codex+"/output_df70data por con_lit orden no import.csv"
file_path2 = "results/output_df90"+ codex +"data por"+por+"_sorted.csv"

df2 = pd.read_csv(file_path2,  encoding = 'utf-8') 
df2 = df2.rename(columns = {'INV':'INV1'})
file_path = "data_new.xlsx"
df = pd.read_excel(file_path, sheetname='tituli', encoding='utf-8') 
print('output', len(df2))
#df1 = df[df['INV'].isin(df2['INV'])].reset_index(drop = False)
print('original', len(df))
# use this merge when you're doing ALL not just one per amphora
#df_final = df1.merge(df2, left_index = True, right_index = True)
df_final = pd.merge(df, df2, left_on = 'INV', right_on = 'INV1')

print('final', len(df_final))

#df_final.to_csv('results/'+codex+'/merged_'+ codex + file_path2[15:], encoding='utf_8_sig')
df_final.to_csv('results/merged_'+ file_path2[15:], encoding='utf_8_sig')

