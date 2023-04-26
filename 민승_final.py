#%%
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:15:16 2022

@author: yoon0
"""

import numpy as np
import pandas as pd

import os
# dir_path = os.chdir("C:/Users/yoon0/Desktop/민승/ms_data/db")
# file_list = os.listdir(dir_path)
# print(file_list)
#%% real data 
C0s = pd.read_csv('C0s_final.csv', encoding = 'cp949', index_col = 0)
A=  pd.read_csv('공간특성_final.csv', index_col = 0)
materials=  pd.read_csv( '물질특성_죄종.csv', index_col = 0)
kmas =  pd.read_csv('kmas_final.csv', index_col = 0)
Q =  pd.read_csv('Q_final.csv', encoding = 'cp949', index_col = 0)

chemical_list = materials.index
scenario_list = Q.index
source_list = kmas.index[0: len(A.columns)]
A.columns = source_list

hm = materials['hm']
kp = materials['kp']
kdust = materials['kdust']
def devision(df, x):
    division_df= df[df.시나리오 ==x].drop(['시나리오'], axis=1)
    return division_df

#%% 분자
def numer(i): # i : 시나리오 번호 ,0~15
    x = scenario_list[i]
    C0 = devision(C0s,x)
    kma = devision(kmas,x)
    kma_inv = 1/kma
    kma_inv.replace([np.inf, -np.inf], 0, inplace=True)
    A_i_want = A.loc[x]
    
    formula1 = np.multiply(kma_inv, C0 ).transpose() # kma * C0
    formula2 =  formula1.dot(A_i_want) # sigma_i(A) * kma * C0
    formula3 = np.multiply(hm,formula2) #  hm*sigma_i(A) * kma * C0
    num = pd.DataFrame(formula3, columns = [x])
    return num

numerator = pd.concat(map(numer,range(0,len(scenario_list))), axis = 1).transpose()
#%% 분모
tsp = 20
vt = 6

botA = A.sum(axis=1)
# Q,  𝑄(𝑠)
Q_expand = np.full( len(chemical_list),1)
term0 =np.multiply( np.array(Q), Q_expand.T) 
# tsp*Q*kp , elementarywise product , #sc x #chm ,  𝑄(𝑠)×𝑇𝑠𝑝×𝐾𝑝(𝑐) 
term1 = tsp*np.multiply( np.array(Q), np.array(kp).T) 
# #sc x #chm,  𝑉𝑡×𝑇𝑠𝑝×𝐾𝑝(𝑐)×𝐴_𝑏𝑜𝑡 (𝑠) 
term2 = vt*tsp*np.multiply(np.array(botA).reshape(len(botA),1), np.array(kp).reshape(1,len(kp))) 
# h𝑚(𝑐)×∑𝐴_𝑖 (k) 
term3 =np.matmul( np.array(A.sum(axis=1)).reshape(len(scenario_list),1) , np.array(hm).reshape(1,len(chemical_list)))

denomitor = term0 + term1 + term2 + term3

#%% 기여율
y = numerator/denomitor
# dust농도 = air농도 / kdust
y_dust = y.mul(kdust, axis = 1)

# %%
