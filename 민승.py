# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 18:15:16 2022

@author: yoon0
"""

import numpy as np
import pandas as pd

import os
# # dir_path = os.chdir("C:/Users/yoon0/Desktop/민승/ms_data/db")
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
print(list(map(numer, range(0,len(scenario_list)))))

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
weight = A.div( A.sum(axis=1), axis = 0)
# dust농도 = air농도 / kdust
y_dust = y.mul(kdust, axis = 1)

y.to_csv('y.csv',encoding = 'cp949')
y_dust.to_csv('y_dust.csv',encoding = 'cp949' )

#%% old example
scenario_index = np.arange(0,14)
scenario_list = list( map(lambda x: '시나리오'+ str(x), scenario_index))

source_index = np.arange(0,20)
source_list = list(map(lambda x : '배출원'+ str(x), source_index))

chemical_index =np.arange(0,8)
chemical_list =list( map(lambda x : '화학물질'+str(x), chemical_index))

dt = np.random.rand(len(chemical_list),3)
materials= pd.DataFrame(data = dt, columns=['hm','kp','kdust'], index = chemical_list) # 물질특성 hm ,kp, kdust

dt2 =np.random.rand(len(scenario_list),len(source_list))
spaces = pd.DataFrame(data =dt2, index = scenario_list,columns = source_list) # A_i
#%%
bot_A =np.random.rand(len(scenario_list))
botA = pd.DataFrame(data=bot_A, index = scenario_list, columns = ['bottomA']) # A_bottom
#%%
Q_dt =np.random.rand(len(scenario_list))
Q = pd.DataFrame(data=Q_dt, columns=['Q'], index = scenario_list)

def sc(i):
    asdf = np.random.rand(len(source_list), len(chemical_list))
    cas = pd.DataFrame(data= asdf,columns =chemical_list, index =source_list )
    cas.insert(0, 'scenario',scenario_list[i])
    return cas

C0s = pd.concat(map(sc, scenario_index))
kmas = pd.concat( map(sc, scenario_index))
#%% 분자 hm*sigma_i(A) * kma * C0

def condition(x):
    A_i_want = spaces.loc[x]
    C0_i_want = C0s[C0s.scenario ==x].drop(['scenario'], axis=1)
    kma_i_want = kmas[kmas.scenario ==x].drop(['scenario'], axis=1)
    
    formula1 = np.multiply(kma_i_want, C0_i_want ).transpose() # kma * C0
    formula2 =  formula1.dot(A_i_want) # sigma_i(A) * kma * C0
    formula3 = np.multiply(hm,formula2) #  hm*sigma_i(A) * kma * C0
    
    num = pd.DataFrame(formula3, columns = [x])
    return num

numerator = pd.concat(map(condition,scenario_list), axis = 1).transpose()
#%% 분모
tsp = 1.5
vt = 0.6
kp = materials['kp']
# Q,  𝑄(𝑠)
Q_expand = np.full( len(chemical_list),1)
term0 =np.multiply( np.array(Q), Q_expand.T) #14x8

# tsp*Q*kp , elementarywise product , 14x8 ,  𝑄(𝑠)×𝑇𝑠𝑝×𝐾𝑝(𝑐) 
term1 = tsp*np.multiply( np.array(Q), np.array(kp).T) 
# 14x8 # 𝑉𝑡×𝑇𝑠𝑝×𝐾𝑝(𝑐)×𝐴_𝑏𝑜𝑡 (𝑠) 
term2 = vt*tsp*np.multiply(np.array(botA), np.array(kp).T) 
# h𝑚(𝑐)×∑𝐴_𝑖 (k) 
term3 =np.matmul( np.array(spaces.sum(axis=1)).reshape(len(scenario_list),1) , np.array(hm).reshape(1,len(chemical_list)))


denomitor = term0 + term1 + term2 + term3
#%% 값
y = numerator/denomitor
#ex. s1 =바닥재(PVC), 실크벽지, 의자(mdf), 선반(mdf) , c0 = dehp
print (numerator.iloc[5,6]/denomitor[5,6])
print(y.iloc[5,6])
#%% 기여율
weight = spaces.div( spaces.sum(axis=1), axis = 0)
# dust농도 = air농도 / kdust
k_dust = materials['kdust']
y_dust = y.div(k_dust, axis = 1)

