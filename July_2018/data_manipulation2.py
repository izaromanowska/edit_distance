# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 11:59:13 2017

@author: iar1g09
"""

from __future__ import division
import pandas as pd
#import editdistance

#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
# path of the data file to be analysed
file_path = "data_new.xlsx"

# which column to use 
column1 = 'CODEX 4'

# min no of characters in the string
length_tituli = 1

# Would you like to sort the characters alphabetically (i.e., their order is not important)
# 1 - yes, please 0 - no, thanks
# sortitout = 0

#type_analysis = 0
# 0 - por conceptum, 1 - por literae, 2 - por ambos

def read_data(file_path, column1):
    """ Here we read the data, wrangle it in a shape we need, and clean it,
    1. read the excel sheets - the tituli one and the object one,
    2. create the addresses (e.g., the address of an aedificium is it's regio + insula + aedificium no),
    3. in the addresses, replace 'n' and 'INC' which indicate 'unknown' with a zero,
    4. merge it with the titulli data frame so that each titulli has a location, 
    5. subset the data to columns you need and give them the right names
    
    """ 
    #  1. read the excel sheets - the tituli one and the object one
    df = pd.read_excel(file_path, covert_float = True, sheetname='tituli', encoding = 'utf-8') 
    df2 = pd.read_excel(file_path, covert_float = True, sheetname = 'objeto', encoding = 'utf-8')
    df_org = df.copy()
 
    #  2. create the addresses (e.g., the address of an aedificium is it's regio + insula + aedificium no)
    
#    df2.REGIO.fillna(0,inplace = True)
    df2['locR'] = df2[['REGIO']].apply(lambda x: ''.join(x.fillna(0).astype(str)),axis=1)

    df2['locI'] = df2[['REGIO','INSULA']].apply(lambda x: ''.join(x.fillna(0).astype(str)),axis=1)
    df2['locA'] = df2[['REGIO','INSULA','AEDIFICIUM']].apply(lambda x: ''.join(x.fillna(0).astype(str)),axis=1)
    
    #  3. in the addresses, replace 'n' and 'INC' which indicate 'unknown' with a zero
    
    for i in ['locR', 'locI', 'locA']:
        df2[i] = df2[i].str.replace("n","0")
        df2[i] = df2[i].str.replace("INC","0")
#        df2[i] = df2[i].str.replace("extra moe0ia","0")
        
    #  4. merge it with the titulli data frame so that each titulli has a location    
    
    df = pd.merge(df, df2, on = 'INV')
    
    #  5. subset the data to columns you need 
    
    df = df[['INV', column1, 'concepta', 'REGESTUM', 'LITTERAE', 'CONCEPTUM', 'locR', 'locI', 'locA' ]] #[:100]   
    df.rename(columns={column1 : 'CODEX'}, inplace = True)

    assert (len(df) == len(df_org)), 'Some rows have been deleted'
    return df

from unidecode import unidecode
def remove_non_ascii(text):
     return unidecode(str(text))


def clean_data (df, sortitout): 
    """     
    1. clear up the slashes (not actually used in this version of codex) 
    2. subset the data to strings longer than the specified number of characters 'concepta'
    3. only now remove nans and reset the index (because we removed some of the rows)
    4. If the data is to be sorted (i.e., the order of caracters in unimportant), it will be done here
    5. convert the INV column into integers
    """
    df_org = df.copy()
    #  1. clear up the slashes (not actually used in this version of codex) 
    df['CODEX'] = df['CODEX'].str.replace("//","1")
    df['CODEX'] = df['CODEX'].str.replace("/=","2")
    

    #  2. subset the data to strings longer than the specified number of characters
    
    df = df[df['concepta']>= length_tituli]
    
    assert ((df.concepta>=length_tituli).all().all()), 'some values are too small' 

    #    This is an alternative implementation in which you can actually count the caracters rather than depend on the number in another column
    #    This is done for 1 and for two columns for instances when we merge the titulli with e.g., the colour (tinta)
    #   df = df[df[column1].map(len) > length_tituli]
    #   df = df[df[column2].map(len) > length_tituli]
    
    #   3. only now remove nans, if any, and reset the index (because we removed some of the rows)

    df = df.dropna()
    df = df.reset_index(drop = True)
    assert (len(df_org[df_org['concepta']>= length_tituli]) == len(df)), 'rows have been lost'

    #   4. If the data is to be sorted (i.e., the order of caracters in unimportant), it will be done here
    #   Also, a suffix will be attached to the results to distinguish outputs that are and that are not sorted   
    
    if sortitout:        
        df['CODEX'] = df['CODEX'].apply(lambda x: ''.join(sorted(x)))
        title = '_sorted'
    else: 
        title = '_unsorted'

    #   5. convert the INV column into integers
    df['INV'] = df['INV'].astype(int)
    
    return df, title

def aproximacion_por_conceptum(df):
    """ Approximacion por conceptum means that the concept value will be doubled"""
    
    df['CODEX'] = df['CODEX'].str.replace("N","NN")
    df['CODEX'] = df['CODEX'].str.replace("n","Nn")
    df['CODEX'] = df['CODEX'].str.replace("P","PP")
    df['CODEX'] = df['CODEX'].str.replace("p","Pp")
    df['CODEX'] = df['CODEX'].str.replace("X","XX")
    df['CODEX'] = df['CODEX'].str.replace("x","Xx")
    df['CODEX'] = df['CODEX'].str.replace("C","CC")
    df['CODEX'] = df['CODEX'].str.replace("c","Cc")
    df['CODEX'] = df['CODEX'].str.replace("S","SS")
    df['CODEX'] = df['CODEX'].str.replace("s","Ss")
    df['CODEX'] = df['CODEX'].str.replace("I","II")
    df['CODEX'] = df['CODEX'].str.replace("i","Ii")

    return df    
    
def aproximacion_por_literae(df):
    """ Approximacion por literae means that the literae value will be doubled"""

    df['CODEX'] = df['CODEX'].str.replace("N","Nl")
    df['CODEX'] = df['CODEX'].str.replace("n","ng")
    df['CODEX'] = df['CODEX'].str.replace("P","Pl")
    df['CODEX'] = df['CODEX'].str.replace("p","pg")
    df['CODEX'] = df['CODEX'].str.replace("X","Xl")
    df['CODEX'] = df['CODEX'].str.replace("x","xg")
    df['CODEX'] = df['CODEX'].str.replace("C","Cl")
    df['CODEX'] = df['CODEX'].str.replace("c","cg")
    df['CODEX'] = df['CODEX'].str.replace("S","SS")
    df['CODEX'] = df['CODEX'].str.replace("s","ss")
    df['CODEX'] = df['CODEX'].str.replace("I","Il")
    df['CODEX'] = df['CODEX'].str.replace("i","ig")   
    
    return df  
    
    
def aproximacion_por_con_lit(df):
    """ Approximacion por conceptum & litterae means that the both values will be doubled - so that they become equally important"""

    df['CODEX'] = df['CODEX'].str.replace("N","NNl")
    df['CODEX'] = df['CODEX'].str.replace("n","Nng")
    df['CODEX'] = df['CODEX'].str.replace("P","PPl")
    df['CODEX'] = df['CODEX'].str.replace("p","Ppg")
    df['CODEX'] = df['CODEX'].str.replace("X","XXl")
    df['CODEX'] = df['CODEX'].str.replace("x","Xxg")
    df['CODEX'] = df['CODEX'].str.replace("C","CCl")
    df['CODEX'] = df['CODEX'].str.replace("c","Ccg")
    df['CODEX'] = df['CODEX'].str.replace("S","SSS")
    df['CODEX'] = df['CODEX'].str.replace("s","Sss")
    df['CODEX'] = df['CODEX'].str.replace("I","IIl")
    df['CODEX'] = df['CODEX'].str.replace("i","Iig")
     
    return df  
    


def main(file_path, type_analysis, sortitout):
    
    """ wrapper: read data, clean it and run the analysis, save the results """
    data = read_data(file_path, column1)
    
    c_data, title = clean_data(data, sortitout)
#    df = df.apply(remove_non_ascii)
    print(len(c_data))
    if type_analysis == 0:
        data_por_conceptum = aproximacion_por_conceptum(c_data)
        data_por_conceptum.to_csv( column1 +"data por con" + title + ".csv", index = False, encoding='utf-8')
  
    if type_analysis == 1:
        data_por_literae = aproximacion_por_literae(c_data)
        data_por_literae.to_csv( column1 +"data por lit" + title + ".csv", index = False, encoding='utf-8')
  
    if type_analysis == 2:
        data_por_con_lit = aproximacion_por_con_lit(c_data)
        data_por_con_lit.to_csv( column1 +"data por con_lit" + title + ".csv", index = False, encoding='utf-8')
 
# Testing, run the code for all types of analysis, with and without sorting the values    
for type_analysis in range(3):
    for sortitout in range(2):
        main(file_path, type_analysis, sortitout)    
    