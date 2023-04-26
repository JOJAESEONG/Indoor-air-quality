"""
Created on Mon Jun 27 15:37:19 2022

@author: Panel: js.jo, Algorithm: gwyoo & dykwak
"""


# In[] model load
import pandas as pd
import panel as pn
# import dask.dataframe as dd
import numpy as np
import plotly.io as pio
import matplotlib.pyplot as plt
import os
RAW_CSS = """
.mdc-drawer {
background: #FAFAFA; /* GRAY 50 */
width: 1000px !important;
}

.mdc-drawer.mdc-drawer--open:not(.mdc-drawer–closing)+.mdc-drawer-app-content {
margin-left: 1000px !important;
}
"""
pio.renderers.default='notebook'
pn.extension('plotly',sizing_mode='stretch_width',raw_css=[RAW_CSS])
# %%

dir_path = os.chdir("C:/Users/gwyoo/Downloads/living_environment (2)")

list_1=pd.read_csv("물질특성_죄종.csv", index_col=0,thousands = ',')
kmas =  pd.read_csv('kmas_final.csv', index_col = 0)
cas_rn=list_1.index
cas_rn_val=cas_rn.values
cas_rn_val=cas_rn_val.tolist()
cas_rn_val.insert(0,'')
chemical_list=cas_rn_val.copy()
select_cami=pn.widgets.Select(name='물질 리스트', options=chemical_list, value='', sizing_mode='fixed')
# %%
# 물질특성
text_input = pn.widgets.TextInput(name='hm (m/h)',value='',sizing_mode='fixed',width=120)
text_input2 = pn.widgets.TextInput(name='kp (m3/μg)',value='',sizing_mode='fixed',width=120)
text_input3 = pn.widgets.TextInput(name='kdust',value='',sizing_mode='fixed',width=120)
widget_box2=pn.Column(text_input, text_input2, text_input3)

# kma 입력 
#시나리오0
text_input6 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input7 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input8 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input9 = pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input10 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input11 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box0=pn.Column(pn.Row(text_input6,text_input7,text_input8),pn.Row(text_input9,text_input10,text_input11))

#시나리오1
text_input12 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input13 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input14 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input15= pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input16 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input17 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box1=pn.Column(pn.Row(text_input12,text_input13,text_input14),pn.Row(text_input15,text_input16,text_input17))

#시나리오2
text_input18 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input19 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input20 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input21= pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input22 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input23 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box2=pn.Column(pn.Row(text_input18,text_input19,text_input20),pn.Row(text_input21,text_input22,text_input23))

#시나리오3
text_input24 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input25 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input26 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input27= pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input28 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input29 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box3=pn.Column(pn.Row(text_input24,text_input25,text_input26),pn.Row(text_input27,text_input28,text_input29))

#시나리오4
text_input30 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input31 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input32 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input33= pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input34 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input35 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box4=pn.Column(pn.Row(text_input30,text_input31,text_input32),pn.Row(text_input33,text_input34,text_input35))

#시나리오5
text_input36 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input37 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input38 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input39= pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input40 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input41 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box5=pn.Column(pn.Row(text_input36,text_input37,text_input38),pn.Row(text_input39,text_input40,text_input41))
# %%
# kma 입력 
#시나리오6
text_input42 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input43 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input44 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input45 = pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input46 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input47 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box6 = pn.Column(pn.Row(text_input42,text_input43,text_input44),pn.Row(text_input45,text_input46,text_input47))

#시나리오7
text_input48 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input49 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input50 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input51 = pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input52 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input53 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box7 = pn.Column(pn.Row(text_input48,text_input49,text_input50),pn.Row(text_input51,text_input52,text_input53))

#시나리오8
text_input54 = pn.widgets.TextInput(name='mdf',value='',sizing_mode='fixed',width=120)
text_input55 = pn.widgets.TextInput(name='PVC tile',value='',sizing_mode='fixed',width=120)
text_input56 = pn.widgets.TextInput(name='PVC floor', value='',sizing_mode='fixed',width=120)
text_input57 = pn.widgets.TextInput(name='종이벽지', value='',sizing_mode='fixed',width=120)
text_input58 = pn.widgets.TextInput(name='실크벽지', value='',sizing_mode='fixed',width=120)
text_input59 = pn.widgets.TextInput(name='paint', value='',sizing_mode='fixed',width=120)
senario_box8 = pn.Column(pn.Row(text_input54,text_input55,text_input56),pn.Row(text_input57,text_input58,text_input59))

# %%
side_tab=pn.Tabs(
    ('시나리오0',senario_box0),
    ('시나리오1',senario_box1),
    ('시나리오2',senario_box2),
    ('시나리오3',senario_box3),
)
# %%
side_tab2=pn.Tabs(  
    ('시나리오4',senario_box4),
    ('시나리오5',senario_box5),
    ('시나리오6',senario_box6),
    ('시나리오7',senario_box7),
)
# %%
side_tab3=pn.Tabs(  
    ('시나리오8',senario_box7),
)
# %%
button = pn.widgets.Button(name='Calculate', button_type='primary',sizing_mode='fixed',width=120)
button2 = pn.widgets.Button(name='Refresh', button_type='primary',sizing_mode='fixed',width=120)
mark7=pn.pane.Markdown('<br>')
widget_box=pn.Column(pn.pane.Markdown('<br>'),pn.pane.Markdown('## 물질특성 '),widget_box2, pn.pane.Markdown('## <br> KMA값 입력'),side_tab,mark7,side_tab2,mark7,side_tab3,mark7)
# %%
mark=pn.pane.Markdown(' ')
# %%
@pn.depends(x=select_cami.param.value)
def widget_value(x):
    chemi_df=list_1.copy()
    if x == '':
        options=['','','']
    else:
        if (chemi_df.index==x).any():
            values=np.array(chemi_df[chemi_df.index == x]).flatten()
            options=[str(round(values[0],2)),str(round(values[1],2)),str(round(values[2],2))]
    return options
# %%
@pn.depends(x=select_cami.param.value)
def widget_value2(x):
    chemi_df=kmas.copy()
    if x == '':
        options2=['','','','','','','','','','','','','','','','','','','','','']
    else:
        if x in chemi_df.columns:
            df=chemi_df[x]
            options2=df.to_list()
    return options2
# %%
@pn.depends(x=select_cami.param.value)
def side_area(x):
    if x == '':
        side=pn.Column()
    else:
        options=widget_value(x)
        options2=widget_value2(x)
        options2=list(map(str,options2))
        #공통
        text_input.value=options[0]
        text_input2.value=options[1]
        text_input3.value=options[2]
        #kma시작
        text_input6.value=format(float(options2[0]),'.2E')
        text_input7.value=format(float(options2[1]),'.2E')
        text_input8.value=format(float(options2[2]),'.2E')
        text_input9.value=format(float(options2[3]),'.2E')
        text_input10.value=format(float(options2[4]),'.2E')
        text_input11.value=format(float(options2[5]),'.2E')
        text_input12.value=format(float(options2[6]),'.2E')
        text_input13.value=format(float(options2[7]),'.2E')
        text_input14.value=format(float(options2[8]),'.2E')
        text_input15.value=format(float(options2[9]),'.2E')
        text_input16.value=format(float(options2[10]),'.2E')
        text_input17.value=format(float(options2[11]),'.2E')
        text_input18.value=format(float(options2[12]),'.2E')
        text_input19.value=format(float(options2[13]),'.2E')
        text_input20.value=format(float(options2[14]),'.2E')
        text_input21.value=format(float(options2[15]),'.2E')
        text_input22.value=format(float(options2[16]),'.2E')
        text_input23.value=format(float(options2[17]),'.2E')
        text_input24.value=format(float(options2[18]),'.2E')
        text_input25.value=format(float(options2[19]),'.2E')
        text_input26.value=format(float(options2[20]),'.2E')
        text_input27.value=format(float(options2[21]),'.2E')
        text_input28.value=format(float(options2[22]),'.2E')
        text_input29.value=format(float(options2[23]),'.2E')
        text_input30.value=format(float(options2[24]),'.2E')
        text_input31.value=format(float(options2[25]),'.2E')
        text_input32.value=format(float(options2[26]),'.2E')
        text_input33.value=format(float(options2[27]),'.2E')
        text_input34.value=format(float(options2[28]),'.2E')
        text_input35.value=format(float(options2[29]),'.2E')
        text_input36.value=format(float(options2[30]),'.2E')
        text_input37.value=format(float(options2[31]),'.2E')
        text_input38.value=format(float(options2[32]),'.2E')
        text_input39.value=format(float(options2[33]),'.2E')
        text_input40.value=format(float(options2[34]),'.2E')
        text_input41.value=format(float(options2[35]),'.2E')
        text_input42.value=format(float(options2[36]),'.2E')
        text_input43.value=format(float(options2[37]),'.2E')
        text_input44.value=format(float(options2[38]),'.2E')
        text_input45.value=format(float(options2[39]),'.2E')
        text_input46.value=format(float(options2[40]),'.2E')
        text_input47.value=format(float(options2[41]),'.2E')
        text_input48.value=format(float(options2[42]),'.2E')
        text_input49.value=format(float(options2[43]),'.2E')
        text_input50.value=format(float(options2[44]),'.2E')
        text_input51.value=format(float(options2[45]),'.2E')
        text_input52.value=format(float(options2[46]),'.2E')
        text_input53.value=format(float(options2[47]),'.2E')
        text_input54.value=format(float(options2[48]),'.2E')
        text_input55.value=format(float(options2[49]),'.2E')
        text_input56.value=format(float(options2[50]),'.2E')
        text_input57.value=format(float(options2[51]),'.2E')
        text_input58.value=format(float(options2[52]),'.2E')
        text_input59.value=format(float(options2[53]),'.2E')
        side=pn.Row(widget_box,button2)
    return side
# %%
side_area('DEHP')
# %%
"""
Created on Mon Jun 27 15:37:19 2022

@author: gwyoo & dykwak
"""

# 물질선택, 제품 중 농도 입력
chemical = 'DEHP' #'화학물질0'
# --> 모델 돌려서 시나리오별 농도값 산출
# In[]
# 1. receptor df 만들기
receptor_df = pd.read_csv('NF_scenario_new.csv')


kmas_input=pd.DataFrame({'시나리오':['시나리오0','시나리오0','시나리오0','시나리오0','시나리오0','시나리오0','시나리오1','시나리오1','시나리오1','시나리오1','시나리오1','시나리오1','시나리오2','시나리오2','시나리오2','시나리오2','시나리오2','시나리오2','시나리오3','시나리오3','시나리오3','시나리오3','시나리오3','시나리오3','시나리오4','시나리오4','시나리오4','시나리오4','시나리오4','시나리오4','시나리오5','시나리오5','시나리오5','시나리오5','시나리오5','시나리오5','시나리오6','시나리오6','시나리오6','시나리오6','시나리오6','시나리오6','시나리오7','시나리오7','시나리오7','시나리오7','시나리오7','시나리오7','시나리오8','시나리오8','시나리오8','시나리오8','시나리오8','시나리오8']
,str(chemical):[text_input6.value,text_input7.value,text_input8.value,text_input9.value,text_input10.value,text_input11.value,text_input12.value,text_input13.value,
text_input14.value,text_input15.value,text_input16.value,text_input17.value,text_input18.value,text_input19.value,text_input20.value,text_input21.value,text_input22.value,text_input23.value,
text_input24.value,text_input25.value,text_input26.value,text_input17.value,text_input28.value,text_input29.value,text_input30.value,text_input31.value,text_input32.value,text_input33.value,
text_input34.value,text_input35.value,text_input36.value,text_input37.value,text_input38.value,text_input39.value,text_input40.value,text_input41.value,text_input42.value,text_input43.value,
text_input44.value,text_input45.value,text_input46.value,text_input47.value,text_input48.value,text_input49.value,text_input50.value,text_input51.value,text_input52.value,text_input53.value,
text_input54.value,text_input55.value,text_input56.value,text_input57.value,text_input58.value,text_input59.value]},index=['mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint','mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint','mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint',
'mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint','mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint','mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint','mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint',
'mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint','mdf','PVC tile','PVC floor','종이벽지','실크벽지','paint'])    

pd.set_option('display.float_format', '{:.2e}'.format)

#%% real data 
C0s = pd.read_csv('C0s_final.csv', encoding = 'cp949', index_col = 0)
C0s=C0s[['시나리오',chemical]]
A=  pd.read_csv('공간특성_final.csv', index_col = 0)
# materials=  pd.read_csv( '물질특성_죄종.csv', index_col = 0)
kmas =  kmas_input
kmas.set_index(str(chemical))
kmas=kmas.astype({chemical:'float'})
# pd.options.display.float_format = '{:.2f}'.format
Q =  pd.read_csv('Q_final.csv', encoding = 'cp949', index_col = 0)

chemical_list = chemical
#chemical_list = materials.index
scenario_list = Q.index
source_list = kmas.index[0: len(A.columns)]
A.columns = source_list

hm = float(text_input.value)
kp = float(text_input2.value)
kdust = float(text_input3.value)

def devision(df, x):
    division_df= df[df.시나리오 ==x].drop(['시나리오'], axis=1)
    return division_df
#%% 분자
def numer(i): # i : 시나리오 번호 ,0~8
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

# %% 분모
tsp = 20
vt = 6

botA = A.sum(axis=1)
# Q,  𝑄(𝑠)
Q_expand = np.full(1,1)
term0 =np.multiply( np.array(Q), Q_expand.T) 
# tsp*Q*kp , elementarywise product , #sc x #chm ,  𝑄(𝑠)×𝑇𝑠𝑝×𝐾𝑝(𝑐) 
term1 = tsp*np.multiply( np.array(Q), np.array(kp).T) 
# #sc x #chm,  𝑉𝑡×𝑇𝑠𝑝×𝐾𝑝(𝑐)×𝐴_𝑏𝑜𝑡 (𝑠) 
term2 = vt*tsp*np.multiply(np.array(botA).reshape(len(botA),1), np.array(kp).reshape(1,1)) 
# # h𝑚(𝑐)×∑𝐴_𝑖 (k) 
term3 =np.matmul( np.array(A.sum(axis=1)).reshape(len(scenario_list),1) , np.array(hm).reshape(1,1))

denomitor = term0 + term1 + term2 + term3

#%% 기여율
air = numerator/denomitor
air=air[[chemical]]
# dust농도 = air농도 / kdust
y_dust = air.mul(kdust, axis = 1)

y_dust=y_dust[[chemical]]

scenario = ['school_1', 'school_2', 'school_3', 'school_4', 'home_1', 'home_2', 'home_3', 'home_4', 'work_1']

air.index = scenario  ; air.columns = ['c_air']
y_dust.index = scenario  ; y_dust.columns = ['c_dust']

other_c_air = air.iloc[[0,1,2,3,8],:]
home_c_air = air.iloc[4:8,:]
other_c_dust = y_dust.iloc[[0,1,2,3,8],:]
home_c_dust = y_dust.iloc[4:8,:]
# %%

dir_path = os.chdir("C:/Users/gwyoo/Downloads/NF_exposure_2")
data = pd.read_csv('NF_scenario_new.csv', encoding='cp949') #새로운 시나리오 csv 불러오기
# In[] 체중할당

def bw_function(x,y):
    x = int(x)
    y = str(y)
    
    if (10 <= x <= 12) & (y == '남자'):
        return np.random.normal(44.7 ,10.92,500)
    elif (13 <= x <= 15) & (y == '남자'):
        return np.random.normal(61.5 ,13.66,500)
    elif (16 <= x <= 18) & (y == '남자'):
        return np.random.normal(67.3 ,13.97,500)
    elif (19 <= x <= 24) & (y == '남자'):
        return np.random.normal(70.7 ,12.60,500)
    elif (25 <= x <= 34) & (y == '남자'):
        return np.random.normal(75.6 ,12.72,500)
    elif (35 <= x <= 44) & (y == '남자'):
        return np.random.normal(75.2 ,11.84,500)
    elif (45 <= x <= 54) & (y == '남자'):
        return np.random.normal(71.4 ,10.10,500)
    elif (55 <= x <= 64) & (y == '남자'):
        return np.random.normal(68.6 ,9.55,500)
    elif (65 <= x <= 74) & (y == '남자'):
        return np.random.normal(65.6 ,9.33,500)
    elif (75 <= x) & (y == '남자'):
        return np.random.normal(61.7 ,9.01,500)
    
    elif (10 <= x <= 12) & (y == '여자'):
        return np.random.normal(42.7 ,9.95,500)
    elif (13 <= x <= 15) & (y == '여자'):
        return np.random.normal(52.8 ,9.74,500)
    elif (16 <= x <= 18) & (y == '여자'):
        return np.random.normal(56.8 ,9.80,500)
    elif (19 <= x <= 24) & (y == '여자'):
        return np.random.normal(56.0 ,9.77,500)
    elif (25 <= x <= 34) & (y == '여자'):
        return np.random.normal(57.7 ,10.54,500)
    elif (35 <= x <= 44) & (y == '여자'):
        return np.random.normal(58.5 ,9.58,500)
    elif (45 <= x <= 54) & (y == '여자'):
        return np.random.normal(59.0 ,8.69,500)
    elif (55 <= x <= 64) & (y == '여자'):
        return np.random.normal(58.4 ,8.53,500)
    elif (65 <= x <= 74) & (y == '여자'):
        return np.random.normal(57.6 ,8.32,500)
    elif (75 <= x) & (y == '여자'):
        return np.random.normal(53.4 ,9.02,500)
    
bw_df = data.apply(lambda x: bw_function(x['연령'], x['성별코드']), axis=1)
bw_df = pd.DataFrame(bw_df, columns =['bw'])


bw_df = pd.DataFrame(bw_df['bw'].values.tolist()).add_prefix('iteration')#.join(c)
BW_array = np.array(bw_df)
BW_array[BW_array < 0] = 1

# In[]
def IR_function(x):
    if x == 10:
        return np.random.normal(12.23,1.06,500)
    elif x == 11:
        return np.random.normal(12.51,0.61,500)
    elif x == 12:
        return np.random.normal(13.36,1.01,500)
    elif x == 13:
        return np.random.normal(13.97,1.55,500)
    elif x == 14:
        return np.random.normal(14.55,2.33,500)
    elif x == 15:
        return np.random.normal(14.61,1.43,500)
    elif x == 16:
        return np.random.normal(15.16,1.94,500)
    elif x == 17:
        return np.random.normal(14.26,1.31,500)
    elif x == 18:
        return np.random.normal(15.76,2.23,500)
    elif 19 <= x <= 24:
        return np.random.normal(13.09,3.17,500)
    elif 25 <= x <= 34:
        return np.random.normal(14.53,3,500)
    elif 35 <= x <= 44:
        return np.random.normal(15.96,3.17,500)
    elif 45 <= x <= 54:
        return np.random.normal(14.62,3.32,500)
    else:
        return np.random.normal(14.79,2.71,500)

IR_df = data['연령'].apply(IR_function)
IR_df = pd.DataFrame(IR_df)


IR_df = pd.DataFrame(IR_df['연령'].values.tolist()).add_prefix('iteration')#.join(c)
IR_array = np.array(IR_df)
IR_array[IR_array < 0] = 0
# In[]

# 시나리오 부여

# 어린이(13세 미만), 청소년 및 성인 따로 분류
data_child = data[data.연령 < 13]
data_other_work = data[(data.연령 > 12) & ((data.work_daily > 0) | (data.school_daily > 0))]
data_other_home = data[(data.연령 > 12) & ((data.work_daily == 0) & (data.school_daily == 0))]


# 학교 시나리오 분배를 위한 분배비율 default, 사용자가 수정할 경우 그 입력값을 prob로 받아옴
prob = {'school_1': .45,
        'school_2': .05,
        'school_3': .45,
        'school_4': .05} 

# 어린이의 학교 시나리오 분배, 청소년 및 성인의 other (직장 또는 학교) 시나리오 분배, 직장을 다니지 않는 성인의 시나리오 0 분배

data_child.loc[:,'other_sn'] = np.random.choice(list(prob.keys()), size=len(data_child), replace = True, p=list(prob.values()))
data_other_work.loc[:,'other_sn'] = 'work_1'
data_other_home.loc[:, 'other_sn'] = 0

data_1 = pd.concat([data_child, data_other_work, data_other_home], ignore_index=True)
data_1 = data_1.sort_values(by=['가구일련번호', '가구원일련번호'])

# 가정 시나리오 분배를 위한 분배비율 default, 사용자가 수정할 경우 그 입력값을 prob_1로 받아옴
prob_1 = {'home_1': .25,
          'home_2': .25,
          'home_3': .25,
          'home_4': .25}


# 가구별 home_i 시나리오 분배
data_2 = data_1.groupby(['가구일련번호'], as_index=False).size()
data_2.loc[:, 'home_sn'] = np.random.choice(list(prob_1.keys()), size=len(data_2), replace = True, p=list(prob_1.values()))
data_2 = data_2.drop(columns='size')

# 가구별 home 시나리오를 개인별 데이터(data_1)과 합치고 data_3로 통합
data_3 = pd.merge(data_1, data_2, left_on='가구일련번호', right_on='가구일련번호', how='left')


# 활동공간별 농도값을 data 테이블에 합침

data_4 = pd.merge(data_3, other_c_air, left_on='other_sn', right_on=other_c_air.index, how='left')
data_4 = pd.merge(data_4, home_c_air, left_on='home_sn', right_on=home_c_air.index, how='left')
data_4 = pd.merge(data_4, other_c_dust, left_on='other_sn', right_on=other_c_dust.index, how='left')
data_4 = pd.merge(data_4, home_c_dust, left_on='home_sn', right_on=home_c_dust.index, how='left')
data_4.info()
data_4 = data_4.fillna(0) # NAN이 있는 경우 노출량 계산결과가 NAN으로 나오므로, NAN을 0값으로 대체


np_data1 = data_4.to_numpy() # 쉬운 계산을 위하여 numpy array로 변경


# 노출계수 정의
h_c_air = np_data1[:,23].reshape(len(np_data1),1)  #집 공기중 농도
o_c_air = np_data1[:,22].reshape(len(np_data1),1)  #학교, 직장 공기 중 농도
h_c_dust = np_data1[:,25].reshape(len(np_data1),1) #집 먼지 중 농도
o_c_dust = np_data1[:,24].reshape(len(np_data1),1) #학교, 직장 먼지 중 농도

#BW = np_data1[:,17].reshape(len(np_data1),1) #체중
h_d_time_ratio = (np_data1[:,13]/1440).reshape(len(np_data1),1) #주중 집에 24시간 중 머무는 시간 비율
o_d_time_ratio = ( (np_data1[:,14] + np_data1[:,15])/1440 ).reshape(len(np_data1),1) # 주중 학교, 직장에 24시간 중 머무는 시간 비율
h_w_time_ratio = ( np_data1[:,16]/1440 ).reshape(len(np_data1),1) # 주말 집에 24시간 중 머무는 시간 비율

igR = np_data1[:,18].reshape(len(np_data1),1) # 먼지 섭취량


# air exposure = conc * IR * AR / BW,                 air conc = conc * AR
# dust exposure = conc * dust_IgR * AR / BW

exp_inh_air_home_daily = h_c_air * IR_array * h_d_time_ratio / BW_array # 주중 집에 머무는 시간에 대한 실내공기 노출량
exp_inh_air_other_daily = o_c_air * IR_array * o_d_time_ratio / BW_array # 주중 활동공간에 머무는 시간에 대한 실내공기 노출량
exp_inh_air_home_weekend = h_c_air * IR_array * h_w_time_ratio / BW_array # 주말 집에 머무는 시간에 대한 실내공기 노출량

#exp_inh_air_home_daily_sorted = np.sort(exp_inh_air_home_daily, axis=0)
#exp_inh_air_other_daily_sorted = np.sort(exp_inh_air_other_daily, axis=0)
#exp_inh_air_home_weekend_sorted = np.sort(exp_inh_air_home_weekend, axis=0)

#np.min(exp_inh_air_home_daily_sorted, axis = 1)


exp_inh_dust_home_daily = h_c_dust * igR * h_d_time_ratio / BW_array # 주중 집에 머무는 시간에 대한 먼지 노출량
exp_inh_dust_other_daily = o_c_dust * igR * o_d_time_ratio / BW_array # 주중 활동공간에 머무는 시간에 대한 먼지 노출량
exp_inh_dust_home_weekend = h_c_dust * igR * h_w_time_ratio / BW_array # 주말 집에 머무는 시간에 대한 먼지 노출량


# air_conc = conc * AR : 노출량(mg/kg-day)이 아닌 노출농도 계산(mg/m3)
conc_inh_air_home_daily = h_c_air * h_d_time_ratio # 주중 집에 머무는 시간에 대한 실내공기 노출농도
conc_inh_air_other_daily = o_c_air * o_d_time_ratio # 주중 활동공간에 머무는 시간에 대한 실내공기 노출농도
conc_inh_air_home_weekend = h_c_air * h_w_time_ratio # 주말 집에 머무는 시간에 대한 실내공기 노출농도


#일주일 평균 노출량 >> (5* daily exposure(home+other) + 2*weekend exposure )/7
mean_exp_air = ( 5*(exp_inh_air_home_daily + exp_inh_air_other_daily) + (2*exp_inh_air_home_weekend))/7 # 일주일 실내공기 평균 노출량

# 일주일 평균 노출농도 >> (5* daily exposure(home+other) + 2*weekend exposure )/7
mean_conc_air = ( 5*(conc_inh_air_home_daily + conc_inh_air_other_daily) + (2*conc_inh_air_home_weekend))/7 # 일주일 실내공기 평균 노출농도


mean_exp_dust = ( 5*(exp_inh_dust_home_daily + exp_inh_dust_other_daily) + (2*exp_inh_dust_home_weekend))/7 # 일주일 평균 먼지 노출량

total_exp = mean_exp_air + mean_exp_dust # 먼지 + 실내공기 통합 노출량

# In[]
# sort data
mean_exp_air_sorted = np.sort(mean_exp_air, axis=0)
a = np.mean(mean_exp_air_sorted, axis=1)
a_min = np.min(mean_exp_air_sorted, axis=1)
a_max = np.max(mean_exp_air_sorted, axis=1)

mean_exp_air_sorted_5th = mean_exp_air_sorted[int((len(a) - 1) * 0.05),:]
mean_exp_air_sorted_50th = mean_exp_air_sorted[int((len(a) - 1) * 0.5),:]
mean_exp_air_sorted_95th = mean_exp_air_sorted[int((len(a) - 1) * 0.95),:]

range_5th = mean_exp_air_sorted_5th.max() - mean_exp_air_sorted_5th.min()
range_50th = mean_exp_air_sorted_50th.max() - mean_exp_air_sorted_50th.min()
range_95th = mean_exp_air_sorted_95th.max() - mean_exp_air_sorted_95th.min()

np.std(mean_exp_air_sorted_95th)


#calculate CDF values
a_y = 1. * np.arange(len(a)) / (len(a) - 1)

# In[]
#plot CDF
x_list = [np.percentile(a, 5), np.percentile(a, 50), np.percentile(a, 95)]
y_list = [np.percentile(a_y, 5), np.percentile(a_y, 50), np.percentile(a_y, 95)]
err_list = [range_5th, range_50th, range_95th]

plt.plot(a, a_y)
plt.errorbar(x_list, y_list,xerr= err_list, ms=5, ecolor='g', capsize = 10, capthick = 3, ls='none')
plt.xscale('log')

# In[]
pio.renderers.default='browser'
import plotly.express as px
import plotly.graph_objs as go

result_df = pd.DataFrame({'exp':a, 'cdf':a_y})
result_min_df = pd.DataFrame({'exp':a_min, 'cdf':a_y})
result_max_df = pd.DataFrame({'exp':a_max, 'cdf':a_y})

fig = px.line(result_df, x='exp', y='cdf')
fig.show()


# In[]
fig = go.Figure([
    go.Scatter(
        name='Mean',
        x=result_df['exp'],
        y=result_df['cdf'],
        mode='lines',
        line=dict(color='rgb(31, 119, 180)'),
    ),
    go.Scatter(
        name='Upper Bound',
        x=result_max_df['exp'],
        y=result_max_df['cdf'],
        mode='lines',
        marker=dict(color="#444"),
        line=dict(width=0),
        showlegend=False
    ),
    go.Scatter(
        name='Lower Bound',
        x=result_min_df['exp'],
        y=result_min_df['cdf'],
        marker=dict(color="#444"),
        line=dict(width=0),
        mode='lines',
        fillcolor='rgba(68, 68, 68, 0.3)',
        fill='tonexty',
        showlegend=False
    )
])
fig.update_layout(
    yaxis_title='CDF',
    title='노출량',
    hovermode="x"
)
fig.update_layout(xaxis_type="log")
fig.show()