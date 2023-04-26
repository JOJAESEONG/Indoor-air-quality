"""
Created on Mon Jun 27 15:37:19 2022

@author: Panel: js.jo, Algorithm: gwyoo & dykwak
"""
import pandas as pd
import panel as pn
# import dask.dataframe as dd
import numpy as np
from io import BytesIO
import random
import plotly.express as px
import plotly.io as pio
import random
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import hvplot.pandas
import biocide
import markdown
import bokeh.layouts
import bokeh.models
import bokeh.plotting
import bokeh
import plotly.graph_objects as go
import plotly.figure_factory as ff
from bokeh.models import FuncTickFormatter
RAW_CSS = """
.mdc-drawer {
background: #FAFAFA; /* GRAY 50 */
width: 1000px !important;
}

.mdc-drawer.mdc-drawer--open:not(.mdc-drawer–closing)+.mdc-drawer-app-content {
margin-left: 1000px !important;
}

.bk.panel-widget {
  border: None;
  font-size: 20px;
}

.button .bk-btn{
  font-size:20px;
  font-family: NanumBarunGothic;
}

.widget-button .bk-btn {
  font-size:20px;
  font-family: NanumBarunGothic;
}

.table .tabulator {
  font-size: 20px;
}

"""
pio.renderers.default='notebook'
pn.extension('tabulator','plotly',sizing_mode='stretch_width',raw_css=[RAW_CSS])
pd.set_option('display.float_format', '{:.2e}'.format)
list_1=pd.read_csv("물질특성_죄종.csv", index_col=0,thousands = ',')
kmas =  pd.read_csv('kma_six.csv', index_col = 0)
list_2=pd.read_csv("604chemical_default.csv", thousands = ',')
cas_rn=list_1.index
cas_rn_val=cas_rn.values
cas_rn_val=cas_rn_val.tolist()
cas_rn_val.insert(0,'')
chemical_list=cas_rn_val.copy()

select_cami=pn.widgets.Select(name='SVOC_물질 리스트', options=chemical_list, value='', sizing_mode='fixed', css_classes=['panel-widget'])
select_cami2=pn.widgets.Select(name='VOC_물질 리스트', options=chemical_list, value='', sizing_mode='fixed', css_classes=['panel-widget'])
button3 = pn.widgets.Button(name='검색', button_type='primary',sizing_mode='fixed',width=150, css_classes=['button'])

chemi_input= pn.widgets.TextInput(name='화학물질 입력', sizing_mode='fixed',width=150, css_classes=['panel-widget'])
chemi_input2= pn.widgets.TextInput(name='화학물질 입력', value=chemi_input.value, sizing_mode='fixed',width=150, css_classes=['panel-widget'])
radio_group = pn.widgets.RadioBoxGroup(name='노출 산정 방식', options=['간접노출','직접노출','통합노출'], inline=False, css_classes=['panel-widget'])
radio_group_shp=pn.Column(pn.pane.Markdown("## 노출 산정 방식  선택 <br> ", style={'font-family': 'NanumBarunGothic','font-size':'20px'}), radio_group)
radio_group2 = pn.widgets.RadioBoxGroup(name='간접노출 산정 물질 분류 선택', options=['반휘발성 물질 (SVOCs)','휘발성 물질 (VOCs)'], inline=False, css_classes=['panel-widget'])
radio_group_shp2=pn.Column(pn.pane.Markdown("## 물질 선택 <br> ", style={'font-family': 'NanumBarunGothic','font-size':'20px'}), radio_group2)
@pn.depends(xt=radio_group2.param.value)
def selector_2(xt):
    if xt=='반휘발성 물질 (SVOCs)':
        widget=pn.Column(chemi_input,button3)
    elif xt=='휘발성 물질 (VOCs)':
        widget=pn.Column(chemi_input,button3)
    return widget
radio_group3 = pn.widgets.RadioButtonGroup(
    name='Radio Button Group', options=['공간별 노출매체 농도 예측 입력정보', '공간별 노출매체 농도 예측결과', '개인단위 간접 노출량 입력정보','개인 단위 간접 노출량'], sizing_mode='stretch_width', button_type='primary',margin=(0,0,50,0),css_classes=['widget-button'])
radio_group4 = pn.widgets.RadioButtonGroup(
    name='Radio Button Group', options=['공간별 노출매체 농도 예측 입력정보', '공간별 노출매체 농도 예측결과', '개인단위 간접 노출량 입력정보','개인 단위 간접 노출량'], sizing_mode='stretch_width', button_type='primary',margin=(0,0,50,0),css_classes=['widget-button'])
radio_group5 = pn.widgets.RadioButtonGroup(
    name='Radio Button Group2', options=['입력정보확인', '누적노출분포', '제품별노출분포','제품별기여도'], button_type='success',margin=(0,0,50,0),css_classes=['widget-button'])
## sidebar widget
#제품중 농도 (SVOC)
text_input14 = pn.widgets.TextInput(name='paint (㎍/㎥)', value='',sizing_mode='fixed',width=120, margin=(10,30,10,20),css_classes=['panel-widget'])
text_input15 = pn.widgets.TextInput(name='PVC_타일 (㎍/㎥)', value='',sizing_mode='fixed',width=120, margin=(10,30,10,20),css_classes=['panel-widget'])
text_input16 = pn.widgets.TextInput(name='PVC_장판 (㎍/㎥)', value='',sizing_mode='fixed',width=120, margin=(10,30,10,20),css_classes=['panel-widget'])
text_input17 = pn.widgets.TextInput(name='PVC_강화마루 (㎍/㎥)', value='',sizing_mode='fixed',width=120, margin=(10,30,10,20),css_classes=['panel-widget'])
text_input18 = pn.widgets.TextInput(name='종이벽지 (㎍/㎥)',value='',sizing_mode='fixed',width=120, margin=(10,30,10,20),css_classes=['panel-widget'])
text_input19 = pn.widgets.TextInput(name='실크벽지 (㎍/㎥)',value='',sizing_mode='fixed',width=120, margin=(10,30,10,20),css_classes=['panel-widget'])
widget_box4=pn.Column(pn.Row(text_input15, text_input16, text_input17), pn.Row(text_input18, text_input19,text_input14))

#시나리오 분배비율
text_input20 = pn.widgets.TextInput(name='어린이집 1', value='0.12',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input21= pn.widgets.TextInput(name='어린이집 2', value='0.11',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input22 = pn.widgets.TextInput(name='어린이집 3', value='0.11',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input23 = pn.widgets.TextInput(name='어린이집 4', value='0.11',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input24 = pn.widgets.TextInput(name='어린이집 5',value='0.11',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input25 = pn.widgets.TextInput(name='어린이집 6',value='0.11',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input26 = pn.widgets.TextInput(name='어린이집 7', value='0.11',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input27= pn.widgets.TextInput(name='어린이집 8', value='0.11',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input28 = pn.widgets.TextInput(name='어린이집 9', value='0.11',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input29 = pn.widgets.TextInput(name='가정집 1', value='0.25',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input30 = pn.widgets.TextInput(name='가정집 2',value='0.25',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input31 = pn.widgets.TextInput(name='가정집 3',value='0.25',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input32 = pn.widgets.TextInput(name='가정집 4', value='0.25',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input33= pn.widgets.TextInput(name='학교 1', value='0.9',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input34 = pn.widgets.TextInput(name='학교 2', value='0.1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input35 = pn.widgets.TextInput(name='직장', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
widget_box5=pn.Column(pn.Row(text_input20,text_input21,text_input22),pn.Row(text_input23,text_input24,text_input25),pn.Row(text_input26,text_input27,text_input28))
widget_box6=pn.Column(pn.Row(text_input29,text_input30),pn.Row(text_input31,text_input32))
widget_box7=pn.Row(text_input33,text_input34)

##VOC(방출량)
#어린이집
text_input36 = pn.widgets.TextInput(name='가정용 의자 (개)', value='24',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input37 = pn.widgets.TextInput(name='서랍장 (개)', value='6',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input59 = pn.widgets.TextInput(name='신발장 (개)', value='6',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input60 = pn.widgets.TextInput(name='가정용 책상 (개)', value='24',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
#가정
text_input38 = pn.widgets.TextInput(name='신발장 (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input39 = pn.widgets.TextInput(name='가정용책상 (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input40 = pn.widgets.TextInput(name='침대 (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input41 = pn.widgets.TextInput(name='부엌가구 (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input42 = pn.widgets.TextInput(name='서랍장 (개)', value='2',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input43 = pn.widgets.TextInput(name='가정용 의자 (개)', value='2',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input44 = pn.widgets.TextInput(name='TV (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input45 = pn.widgets.TextInput(name='프린터 (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input46 = pn.widgets.TextInput(name='청소기(ON) (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input47 = pn.widgets.TextInput(name='냉장고 (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
widget_box9=pn.Column(pn.Row(text_input38,text_input39,text_input40,text_input41),pn.Row(text_input42,text_input43,text_input44,text_input45),pn.Row(text_input46,text_input47))

#학교 
text_input48 = pn.widgets.TextInput(name='학교 책상 (개)', value='24',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input49 = pn.widgets.TextInput(name='학교 사물함 (개)', value='6',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input50 = pn.widgets.TextInput(name='학교 의자 (개)', value='24',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input51 = pn.widgets.TextInput(name='TV (개)', value='1',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
widget_box10=pn.Column(pn.Row(text_input48,text_input49),pn.Row(text_input50,text_input51))

#회사
text_input52 = pn.widgets.TextInput(name='컴퓨터 (개)', value='10',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input53 = pn.widgets.TextInput(name='모니터 (개)', value='10',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input54 = pn.widgets.TextInput(name='사무용 책상 (개)', value='10',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input55 = pn.widgets.TextInput(name='사무용 의자 (개)', value='10',sizing_mode='fixed',width=120, css_classes=['panel-widget'])
widget_box11=pn.Column(pn.Row(text_input52,text_input53),pn.Row(text_input54,text_input55))
side_tab=pn.Tabs(
    ('어린이집',pn.Column(pn.Row(text_input36,text_input37),pn.Row(text_input59,text_input60))),
    ('가정',widget_box9),
    ('학교',widget_box10),
    ('회사',widget_box11),
    css_classes=['panel-widget']
)
## 직접노출 입력부분
text_input56 = pn.widgets.TextInput(name='분자량 (g/mol)', sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input57 = pn.widgets.TextInput(name='증기압 (at 25℃) (Pa)', sizing_mode='fixed',width=120, css_classes=['panel-widget'])
text_input58 = pn.widgets.TextInput(name='물질명', sizing_mode='fixed',width=350, css_classes=['panel-widget'])
## 사이드바 위젯 확정
button = pn.widgets.Button(name='Calculate', button_type='primary',sizing_mode='fixed',width=120, css_classes=['button'])
button2 = pn.widgets.Button(name='Refresh', button_type='primary',sizing_mode='fixed',width=120, css_classes=['button'])
mark7=pn.pane.Markdown('<br>')
widget_box=pn.Column(pn.pane.Markdown('<br>'),pn.pane.Markdown("# * 활동공간 인체 간접노출량 정보입력", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),mark7,pn.pane.Markdown('### <br> 제품중 농도 입력(㎍/㎥) <br><br> - 선택물질의 제품중 농도를 입력합니다', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),widget_box4,mark7,pn.pane.Markdown('### <br> 시나리오 분배비율 입력 <br><br> -공간별 시나리오를 적용하는 인구집단의 비율을 입력합니다', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.Markdown('### 어린이집 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),widget_box5,pn.pane.Markdown('### 일반가정 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),widget_box6,pn.pane.Markdown('### 학교 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),widget_box7,pn.pane.Markdown('### 직장 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),text_input35,mark7,button)
widget_box8=pn.Column(pn.pane.Markdown("# <br> * 활동공간 인체 간접노출량 정보입력", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.Markdown('### <br> 제품별 시나리오 입력 (가구갯수)', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),side_tab,mark7,pn.pane.Markdown('### <br> 시나리오 분배비율 입력 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.Markdown('### 어린이집 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),widget_box5,pn.pane.Markdown('### 일반가정 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),widget_box6,pn.pane.Markdown('### 학교 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),widget_box7,pn.pane.Markdown('### 직장 <br>', style={'font-family': 'NanumBarunGothic','font-size':'20px'}),text_input35,mark7,button)
widget_box12 = pn.Column(pn.pane.Markdown("# <br> * 생활화학제품 인체직접노출량 정보입력", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),text_input58,text_input56,text_input57,button)
mark=pn.pane.Markdown(' ')
mark2=pn.pane.Markdown('<br>')

total_exposure=pn.Column()

caution_mark=pn.pane.Markdown("### <br> ※ 통합노출은 <br> 간접 & 직접에서 사용된 물질과 동일한 물질로 산정됩니다 <br> 간접 & 직접 노출 산정 후 선택해주세요 <br> ", style={'font-family': 'NanumBarunGothic','font-size':'20px'})

@pn.depends(xt=radio_group.param.value)
def selector(xt):
    if xt=='간접노출':
        widget=pn.Column(radio_group_shp2,selector_2)
    elif xt=='직접노출':
        widget=pn.Column(chemi_input,button3)
    elif xt=='통합노출':
        widget=pn.Column(caution_mark,button)
    return widget

### 선택한 화학물질에 따라 사이드바 표시 위젯과 입력값 결정
from matplotlib.pyplot import text
@pn.depends(button3.param.clicks)
def search_chemi(_):
    # if radio_group.value=='간접노출':
        ##VOC일 경우
    if radio_group.value=='간접노출' and radio_group2.value=='반휘발성 물질 (SVOCs)':
        if chemi_input.value =='':
            side=pn.Column()
        else:
            @pn.depends(x=chemi_input.param.value)
            def widget_value2(x):
                chemi_df=kmas.copy()
                if x == '':
                    options2=['','','','','','']
                else:
                    if (chemi_df.index==x).any():
                        values=np.array(chemi_df[chemi_df.index == x]).flatten()
                        options2=[str(round(values[1],2)),str(round(values[2],2)),str(round(values[3],2)),str(round(values[4],2)),str(round(values[5],2)),str(round(values[6],2))]
                return options2         
            @pn.depends(x=chemi_input.param.value)
            def side_area(x):
                if x == '':
                    side=pn.Column()
                else:
                    options2=widget_value2(x)
                    # options2=list(map(str,options2))
                    #공통
                    # text_input.value=options[0]
                    # text_input2.value=options[1]
                    # text_input3.value=options[2]
                    #kma
                    # text_input6.value=format(float(options2[0]),'.2E')
                    # text_input7.value=format(float(options2[1]),'.2E')
                    # text_input8.value=format(float(options2[2]),'.2E')
                    # text_input9.value=format(float(options2[3]),'.2E')
                    # text_input10.value=format(float(options2[4]),'.2E')
                    # text_input11.value=format(float(options2[5]),'.2E')
                    # 제품중 농도
                    text_input14.value=format(float(options2[5]),'.2E')
                    text_input15.value=format(float(options2[2]),'.2E')
                    text_input16.value=format(float(options2[1]),'.2E')
                    text_input17.value=format(float(options2[0]),'.2E')
                    text_input18.value=format(float(options2[4]),'.2E')
                    text_input19.value=format(float(options2[3]),'.2E')
                    side=pn.Row(widget_box)
                return side
            x=chemi_input.value
            side=side_area(x)
    ##SVOC일 경우
    elif radio_group.value=='간접노출' and radio_group2.value=='휘발성 물질 (VOCs)':
        side=pn.Row(widget_box8)
    elif radio_group.value=='직접노출':
        @pn.depends(x=chemi_input.param.value)
        def widget_value(x):
            chemi_df=list_2.copy()
            if x == '':
                options=['','','','','','','']
            else:
                if (chemi_df['CAS_Num']==x).any():
                    values=np.array(chemi_df[chemi_df['CAS_Num'] == x]).flatten()
                    options=[str(values[0]),str(round(values[2],2)),str(round(values[3],2)),str(format(values[4],'.2E')),str(format(values[5],'.2E')),str(round(values[6],2)),str(format(values[7],'.2E')),str(values[8])]
            return options
        @pn.depends(x=chemi_input.param.value)
        def side_area(x):
            if x == '':
                side=pn.Column()
            else:
                options=widget_value(x)    
                # #직접노출 
                text_input58.value=options[0]
                text_input56.value=options[1]
                text_input57.value=options[4]
    
                side=pn.Row(widget_box12)
            return side
        x=chemi_input.value
        side=side_area(x)
    return side
### 입력값 초기화 이벤트
### 선정된 화학물질로 kma를 DataFrame으로 변환
## 메인 화면 기능
@pn.depends(button.param.clicks)
def calculate_A_batch(_):
    if chemi_input.value =='':
        tabs=pn.Column(pn.pane.JPG('표지.jpg',height=560,width=950,margin=(0,0,50,0)))
    else:
        if radio_group.value=='간접노출' and radio_group2.value== '반휘발성 물질 (SVOCs)':
            """
            Created on Mon Jun 27 15:37:19 2022

            @author: gwyoo & dykwak
            """

            # 물질선택, 제품 중 농도 입력
            chemical = chemi_input.value #'화학물질0'
            # pd.set_option('display.float_format', '{:.2e}'.format)

            #%% real data 
            C0s = pd.read_csv('new C0_농도.csv', encoding = 'cp949', index_col = 0).dropna()
            CAS = chemi_input.value # CAS번호로 대체 필요
            a = float(text_input17.value) # 제품별 농도 입력값
            b = float(text_input15.value) # 제품별 농도 입력값
            c = float(text_input16.value) # 제품별 농도 입력값
            d = float(text_input18.value) # 제품별 농도 입력값
            e = float(text_input19.value) # 제품별 농도 입력값
            f = float(text_input14.value) # 제품별 농도 입력값

            get_conc = [] # 제품별 농도 입력값을 넣을 빈 list만들기
            get_conc.append([a,b,c,d,e,f]) # 빈 List 에 입력값 넣기
            t_get_conc = np.transpose(get_conc) # list 세우기

            #입력받은 CAS번호가 데이터 컬럼명으로 있다면, 데이터컬럼을 입력받은 값으로 df내 칼럼을 대체하고, 없다면, 0을 적용하는 함수 만들기

            def get_cas(N):
                if N in C0s.columns:
                    C0s[N] = t_get_conc
                else :
                    C0s[N] = 0
                return C0s

            C0s=get_cas(chemi_input.value) # 함수 실행

            C0_scenario = pd.read_csv('new C0_시나리오.csv', encoding = 'cp949', index_col = 0).T
            # C0s = pd.read_csv('C0s_final.csv', encoding = 'cp949', index_col = 0)
            # C0s=C0s[['시나리오',chemical]]

            A=  pd.read_csv('공간특성_final.csv', index_col = 0)
            materials=  pd.read_csv( '물질특성_죄종.csv', index_col = 0)
            kmas =  pd.read_csv('kmas_final2.csv', index_col = 0).dropna(axis=1)
            kmas.set_index(str(chemical))
            kmas=kmas.astype({chemical:'float'})
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
                def c0(j):
                    a = C0_scenario[x]
                    b = C0s[j]
                    c = b.multiply(a)
                    return c
                C0 =  pd.concat(map(c0,chemical_list), axis =1, keys = chemical_list)
                kma = devision(kmas,x)
                kma_inv = 1/kma
                kma_inv.replace([np.inf, -np.inf], 0, inplace=True)
                A_i_want = A.loc[x]
                
                formula1 = np.multiply(kma_inv, C0 ).transpose() # 1/kma * C0
                formula2 =  formula1.dot(A_i_want) # sigma_i(A) * 1/kma * C0
                formula3 = np.multiply(hm,formula2) #  hm*sigma_i(A) * 1/kma * C0
                num = pd.DataFrame(formula3, columns = [x])
                return num
            numerator = pd.concat(map(numer,range(0,len(scenario_list))), axis = 1).transpose()
            numerator=numerator[[chemical]]
            #%% 분모
            tsp = 20
            vt = 6

            kp=kp.loc[[chemical]]
            hm=hm.loc[[chemical]]

            botA = A.sum(axis=1)
            # Q,  𝑄(𝑠)
            Q_expand = np.full(1,1)
            term0 =np.multiply( np.array(Q), Q_expand.T) 
            # tsp*Q*kp , elementarywise product , #sc x #chm ,  𝑄(𝑠)×𝑇𝑠𝑝×𝐾𝑝(𝑐) 
            term1 = tsp*np.multiply( np.array(Q), np.array(kp).T) 
            # #sc x #chm,  𝑉𝑡×𝑇𝑠𝑝×𝐾𝑝(𝑐)×𝐴_𝑏𝑜𝑡 (𝑠) 
            term2 = vt*tsp*np.multiply(np.array(botA).reshape(len(botA),1), np.array(kp).reshape(1,1)) 
            # h𝑚(𝑐)×∑𝐴_𝑖 (k) 
            term3 =np.matmul( np.array(A.sum(axis=1)).reshape(len(scenario_list),1) , np.array(hm).reshape(1,1))

            denomitor = term0 + term1 + term2 + term3

            #%% 기여율
            if chemi_input in chemical_list:
                chemical = chemical_list.index(chemi_input)
            y = numerator/denomitor
            # dust농도 = air농도 / kdust
            y_dust = y.mul(kdust, axis = 1)
            y_dust = y_dust[[chemical]]
            y = y[[chemical]]

            y.rename(columns={chemical:'예측된 공기 농도 (㎍/㎥)'},inplace = True)
            y_dust.rename(columns={chemical:'예측된 먼지 농도 (㎍/g)'},inplace = True)
            result=pd.concat([y,y_dust],axis=1)
            result=result.transpose()
            result.columns=['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','가정집1','가정집2','가정집3','가정집4','학교1','학교2','직장']
            result2=result.transpose()
            result2['공간별 시나리오'] = result2.index
            result2.index = range(len(result2))
            result2 = result2[['공간별 시나리오', '예측된 공기 농도 (㎍/㎥)','예측된 먼지 농도 (㎍/g)']]
            result2= result2.style.hide_index()
            tabulator_editors4 = {
                '공간별 시나리오': None,
                '예측된 공기 농도 (㎍/㎥)':None,
                '예측된 먼지 농도 (㎍/g)':None,
            }
            result2_table=pn.widgets.Tabulator(result2,show_index=False,header_align='center',text_align='center',editors=tabulator_editors4,pagination='remote',sizing_mode='fixed',margin=(0,0,55,0),css_classes=['table'])            
            table2=pn.Column(pn.pane.Markdown("## ■ SVOCs 시나리오별 실내환경매체 물질 농도 예측 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'},width=650),result2_table) #,width=650,height=600

####  2번째탭 bar그래프 - air
            y3=pd.read_csv('svoc_air.csv',index_col=0)
            if(y3.index==chemical).any():
                y2=y.copy()
                y2=y2.transpose()
                y2.columns=['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','가정집1','가정집2','가정집3','가정집4','학교1','학교2','직장']
                y2=y2.transpose()

                y3=pd.read_csv('svoc_air.csv',index_col=0)
                y3.loc[[chemical]]

                fig2 = go.Figure(
                    data=[
                        go.Bar(
                            name="예측농도",
                            x=y2.index,
                            y=y2['예측된 공기 농도 (㎍/㎥)'],
                            offsetgroup=0,
                        ),
                        go.Bar(
                            name="실측농도",
                            x=y3["시설"],
                            y=y3["농도"],
                            offsetgroup=1,
                        ),
                    ],
                    layout=go.Layout(
                        title="SVOCs 시나리오별 예측 및 실측 공기 농도 비교 ("+chemical+")",
                        xaxis_title="",
                        yaxis_title="예측된 공기 농도 (㎍/㎥)",
                        width=800, 
                        height=400,

                    )
                )
                fig2.update_yaxes(type='log')

            else:
                y2=y.copy()
                y2=y2.transpose()
                y2.columns=['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','가정집1','가정집2','가정집3','가정집4','학교1','학교2','직장']
                y2=y2.transpose()
                fig2 = px.bar(y2,x=y2.index, y='예측된 공기 농도 (㎍/㎥)')
                fig2.update_yaxes(type='log')
                fig2.update_xaxes(title="")
                fig2.update_layout(width=800, height=400,title="SVOCs 시나리오별 예측 및 실측 공기 농도 비교 ("+chemical+")")

####  2번째탭 bar그래프 - dust
            y4=pd.read_csv('svoc_dust.csv',index_col=0)
            if(y4.index==chemical).any():
                y5=y_dust.copy()
                y5=y5.transpose()
                y5.columns=['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','가정집1','가정집2','가정집3','가정집4','학교1','학교2','직장']
                y5=y5.transpose()

                y4=pd.read_csv('svoc_dust.csv',index_col=0)
                y4.loc[[chemical]]

                fig3 = go.Figure(
                    data=[
                        go.Bar(
                            name="예측농도",
                            x=y5.index,
                            y=y5['예측된 먼지 농도 (㎍/g)'],
                            offsetgroup=0,
                        ),
                        go.Bar(
                            name="실측농도",
                            x=y4["시설"],
                            y=y4["농도"],
                            offsetgroup=1,
                        ),
                    ],
                    layout=go.Layout(
                        title="SVOCs 시나리오별 예측 및 실측 먼지 농도 비교 ("+chemical+")",
                        xaxis_title="",
                        yaxis_title="예측된 먼지 농도 (㎍/g)",
                        width=800, 
                        height=400,
                    )
                )
                fig3.update_yaxes(type='log')

            else:
                y5=y_dust.copy()
                y5=y5.transpose()
                y5.columns=['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','가정집1','가정집2','가정집3','가정집4','학교1','학교2','직장']
                y5=y5.transpose()
                fig3 = px.bar(y5,x=y5.index, y='예측된 먼지 농도 (㎍/g)')
                fig3.update_yaxes(type='log')
                fig3.update_xaxes(title="")
                fig3.update_layout(width=800, height=400,title="SVOCs 시나리오별 예측 및 실측 먼지 농도 비교 ("+chemical+")")



            other_c_air = y.iloc[[0,1,2,3,4,5,6,7,8,13,14,15],:]
            other_c_air=other_c_air.T
            other_c_air.columns=['kinder_1','kinder_2','kinder_3','kinder_4','kinder_5','kinder_6','kinder_7','kinder_8','kinder_9','school_1','school_2','work_1']
            other_c_air=other_c_air.T
            home_c_air = y.iloc[9:13,:]
            home_c_air=home_c_air.T
            home_c_air.columns=['home_1','home_2','home_3','home_4']
            home_c_air=home_c_air.T
            other_c_dust = y_dust.iloc[[0,1,2,3,4,5,6,7,8,13,14,15],:]
            home_c_dust = y_dust.iloc[9:13,:]
            home_c_dust=home_c_dust.T
            home_c_dust.columns=['home_1','home_2','home_3','home_4']
            home_c_dust=home_c_dust.T

            data = pd.read_csv('NF_scenario_new.csv', encoding='cp949') 

            def bw_function(x,y):
                x = int(x)
                y = str(y)

                if (10 <= x <= 12) & (y == '남자'):
                    return np.random.normal(44.7 ,10.92,100)
                elif (13 <= x <= 15) & (y == '남자'):
                    return np.random.normal(61.5 ,13.66,100)
                elif (16 <= x <= 18) & (y == '남자'):
                    return np.random.normal(67.3 ,13.97,100)
                elif (19 <= x <= 24) & (y == '남자'):
                    return np.random.normal(70.7 ,12.60,100)
                elif (25 <= x <= 34) & (y == '남자'):
                    return np.random.normal(75.6 ,12.72,100)
                elif (35 <= x <= 44) & (y == '남자'):
                    return np.random.normal(75.2 ,11.84,100)
                elif (45 <= x <= 54) & (y == '남자'):
                    return np.random.normal(71.4 ,10.10,100)
                elif (55 <= x <= 64) & (y == '남자'):
                    return np.random.normal(68.6 ,9.55,100)
                elif (65 <= x <= 74) & (y == '남자'):
                    return np.random.normal(65.6 ,9.33,100)
                elif (75 <= x) & (y == '남자'):
                    return np.random.normal(61.7 ,9.01,100)

                elif (10 <= x <= 12) & (y == '여자'):
                    return np.random.normal(42.7 ,9.95,100)
                elif (13 <= x <= 15) & (y == '여자'):
                    return np.random.normal(52.8 ,9.74,100)
                elif (16 <= x <= 18) & (y == '여자'):
                    return np.random.normal(56.8 ,9.80,100)
                elif (19 <= x <= 24) & (y == '여자'):
                    return np.random.normal(56.0 ,9.77,100)
                elif (25 <= x <= 34) & (y == '여자'):
                    return np.random.normal(57.7 ,10.54,100)
                elif (35 <= x <= 44) & (y == '여자'):
                    return np.random.normal(58.5 ,9.58,100)
                elif (45 <= x <= 54) & (y == '여자'):
                    return np.random.normal(59.0 ,8.69,100)
                elif (55 <= x <= 64) & (y == '여자'):
                    return np.random.normal(58.4 ,8.53,100)
                elif (65 <= x <= 74) & (y == '여자'):
                    return np.random.normal(57.6 ,8.32,100)
                elif (75 <= x) & (y == '여자'):
                    return np.random.normal(53.4 ,9.02,100)

            bw_df = data.apply(lambda x: bw_function(x['연령'], x['성별코드']), axis=1)
            bw_df = pd.DataFrame(bw_df, columns =['bw'])


            bw_df = pd.DataFrame(bw_df['bw'].values.tolist()).add_prefix('iteration')#.join(c)
            BW_array = np.array(bw_df)
            BW_array[BW_array < 0] = 1


            def IR_function(x):
                if x == 10:
                    return np.random.normal(12.23,1.06,100)
                elif x == 11:
                    return np.random.normal(12.51,0.61,100)
                elif x == 12:
                    return np.random.normal(13.36,1.01,100)
                elif x == 13:
                    return np.random.normal(13.97,1.55,100)
                elif x == 14:
                    return np.random.normal(14.55,2.33,100)
                elif x == 15:
                    return np.random.normal(14.61,1.43,100)
                elif x == 16:
                    return np.random.normal(15.16,1.94,100)
                elif x == 17:
                    return np.random.normal(14.26,1.31,100)
                elif x == 18:
                    return np.random.normal(15.76,2.23,100)
                elif 19 <= x <= 24:
                    return np.random.normal(13.09,3.17,100)
                elif 25 <= x <= 34:
                    return np.random.normal(14.53,3,100)
                elif 35 <= x <= 44:
                    return np.random.normal(15.96,3.17,100)
                elif 45 <= x <= 54:
                    return np.random.normal(14.62,3.32,100)
                else:
                    return np.random.normal(14.79,2.71,100)

            IR_df = data['연령'].apply(IR_function)
            IR_df = pd.DataFrame(IR_df)


            IR_df = pd.DataFrame(IR_df['연령'].values.tolist()).add_prefix('iteration')#.join(c)
            IR_array = np.array(IR_df)
            IR_array[IR_array < 0] = 0


            # 시나리오 부여

            # 어린이(13세 미만), 청소년 및 성인 따로 분류
            data_child = data[data.연령 < 13]
            data_other_work = data[(data.연령 > 12) & ((data.work_daily > 0) | (data.school_daily > 0))]
            data_other_home = data[(data.연령 > 12) & ((data.work_daily == 0) & (data.school_daily == 0))]

            # 학교 시나리오 분배를 위한 분배비율 default, 사용자가 수정할 경우 그 입력값을 prob로 받아옴
            prob = {'school_1': float(text_input33.value),
                    'school_2': float(text_input34.value),
                    } 

            # 어린이의 학교 시나리오 분배, 청소년 및 성인의 other (직장 또는 학교) 시나리오 분배, 직장을 다니지 않는 성인의 시나리오 0 분배

            data_child.loc[:,'other_sn'] = np.random.choice(list(prob.keys()), size=len(data_child), replace = True, p=list(prob.values()))
            data_other_work.loc[:,'other_sn'] = 'work_1'
            data_other_home.loc[:, 'other_sn'] = 0

            data_1 = pd.concat([data_child, data_other_work, data_other_home], ignore_index=True)
            data_1 = data_1.sort_values(by=['가구일련번호', '가구원일련번호'])

            # 가정 시나리오 분배를 위한 분배비율 default, 사용자가 수정할 경우 그 입력값을 prob_1로 받아옴
            prob_1 = {'home_1': float(text_input29.value),
                    'home_2': float(text_input30.value),
                    'home_3': float(text_input31.value),
                    'home_4': float(text_input32.value)}
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
            total_exp_sorted = np.sort(total_exp, axis=0)
            total_exp_sorted_idx = np.argsort(total_exp, axis=0)

            a = np.mean(total_exp_sorted, axis=1)
            a_min = np.min(total_exp_sorted, axis=1)
            a_max = np.max(total_exp_sorted, axis=1)

            total_exp_sorted_5th = total_exp_sorted[int((len(a) - 1) * 0.05),:]
            total_exp_sorted_50th = total_exp_sorted[int((len(a) - 1) * 0.5),:]
            total_exp_sorted_95th = total_exp_sorted[int((len(a) - 1) * 0.95),:]

            #calculate CDF values
            a_y = 1. * np.arange(len(a)) / (len(a) - 1)

            result_df = pd.DataFrame({'exp':a, 'cdf':a_y})
            result_df['chemi']=str(chemical)
            result_df.to_csv('indirect.csv')
            result_min_df = pd.DataFrame({'exp':a_min, 'cdf':a_y})
            result_max_df = pd.DataFrame({'exp':a_max, 'cdf':a_y})

            def line_fig(a,b,c):
                fig5 = go.Figure([
                    go.Scatter(
                        name='Mean',
                        x=a['exp'], #result_df
                        y=a['cdf'],
                        mode='lines',
                        line=dict(color='rgb(31, 119, 180)'),
                    ),
                    go.Scatter(
                        name='Upper Bound',
                        x=b['exp'], #result_max_df
                        y=b['cdf'],
                        mode='lines',
                        marker=dict(color="#444"),
                        line=dict(width=0),
                        showlegend=False
                    ),
                    go.Scatter(
                        name='Lower Bound',
                        x=c['exp'], #result_min_df
                        y=c['cdf'],
                        marker=dict(color="#444"),
                        line=dict(width=0),
                        mode='lines',
                        fillcolor='rgba(68, 68, 68, 0.3)',
                        fill='tonexty',
                        showlegend=False
                    )
                ])

                fig5.update_layout(
                    xaxis_title='노출량 (ng/kg/day)',
                    yaxis_title='CDF',
                    title='노출량 (ng/kg/day)',
                    hovermode="x",
                    width=850,
                    height=550,
                )
                fig5.update_layout(xaxis_type="log")
                return pn.Column(fig5,sizing_mode='fixed',margin=(0,100,0,0))

##### 마지막탭 내용
            idx1 = list(data_4[(10 <= data_4['연령']) & (data_4['연령'] <= 19)].index)
            idx2 = list(data_4[(20 <= data_4['연령']) & (data_4['연령'] <= 29)].index)
            idx3 = list(data_4[(30 <= data_4['연령']) & (data_4['연령'] <= 39)].index)
            idx4 = list(data_4[(40 <= data_4['연령']) & (data_4['연령'] <= 49)].index)
            idx5 = list(data_4[50 <= data_4['연령']].index)

            idx1_mean = np.mean(total_exp[idx1,:], axis=1)
            idx2_mean = np.mean(total_exp[idx2,:], axis=1)
            idx3_mean = np.mean(total_exp[idx3,:], axis=1)
            idx4_mean = np.mean(total_exp[idx4,:], axis=1)
            idx5_mean = np.mean(total_exp[idx5,:], axis=1)

            idx1_500_mean = np.mean(total_exp[idx1,:], axis=0)
            idx2_500_mean = np.mean(total_exp[idx2,:], axis=0)
            idx3_500_mean = np.mean(total_exp[idx3,:], axis=0)
            idx4_500_mean = np.mean(total_exp[idx4,:], axis=0)
            idx5_500_mean = np.mean(total_exp[idx5,:], axis=0)

            def exp_table(mu,std):
                return str(format(mu,'.2E')) + "(±" + str(format(std,'.2E')) + ")"

                
            idx1_min = idx1_500_mean.min()

            v1 = exp_table(idx1_500_mean.mean(), np.std(idx1_500_mean))
            v2 = exp_table(idx2_500_mean.mean(), np.std(idx2_500_mean))
            v3 = exp_table(idx3_500_mean.mean(), np.std(idx3_500_mean))
            v4 = exp_table(idx4_500_mean.mean(), np.std(idx4_500_mean))
            v5 = exp_table(idx5_500_mean.mean(), np.std(idx5_500_mean))

            age_list = ['10대', '20대', '30대', '40대', '50대 이상']

            exposure_table = pd.DataFrame({'연령': age_list,'노출량 (ng/kg/day)': [v1,v2,v3,v4,v5]})
            exposure_table=exposure_table.style.hide_index()
            tabulator_editors5 = {
                '연령': None,
                '노출량 (ng/kg/day)':None
            }

            table_x=pn.widgets.Tabulator(exposure_table,show_index=False,header_align='center',text_align='center',editors=tabulator_editors5,pagination='remote',sizing_mode='fixed',margin=(150,0,25,0),css_classes=['table'])

            # table_x=pn.Column(exposure_table,width=800,height=400)


###########################
            #입력정보화면
            materials2=materials.loc[[chemical]]
            materials2.columns=['화학물질','Mass transfer coef (hm)(m/h)','Particle air partition coef (kp)','Dust-air partition coef. (Kdust)']
            materials2=materials2.transpose()
            tabulator_editors = {
                chemical: None,
            }
            materials2_table=pn.widgets.Tabulator(materials2,header_align='center',text_align='center',editors=tabulator_editors,pagination='remote',sizing_mode='fixed',margin=(0,0,15,0),css_classes=['table'])
            mark3=pn.pane.Markdown("#### ■ Mass transfer coefficient : 물질전달계수 <br> ■ Paticle-air partition coefficient : 입자-공기 분배계수 <br> ■ Dust-air partition coefficient : 먼지-공기 분배계수 ", style={'font-family': 'NanumBarunGothic','font-size':'15px'})

            kmass =  pd.read_csv('kma_six.csv', index_col = 0)
            kmas2=kmass.loc[[chemical]]
            kmas2=kmas2.transpose()
            kmas2_table=pn.widgets.Tabulator(kmas2,header_align='center',text_align='center',editors=tabulator_editors,pagination='remote',sizing_mode='fixed',margin=(0,0,95,0),css_classes=['table'])

            pro_density = pd.DataFrame({'재질':['강화마루 (㎍/㎥)','PVC_장판 (㎍/㎥)','PVC_타일 (㎍/㎥)','실크벽지 (㎍/㎥)','종이벽지 (㎍/㎥)','paint (㎍/㎥)'],'농도 (㎍/㎥)':[text_input17.value,text_input16.value,text_input15.value,text_input19.value,text_input18.value,text_input14.value]})
            pro_density=pro_density.style.hide_index()
            tabulator_editors2 = {
                '재질': None,
                '농도 (㎍/㎥)':None,
            }
            pro_density_table=pn.widgets.Tabulator(pro_density,header_align='center',text_align='center',show_index=False,editors=tabulator_editors2,pagination='remote',sizing_mode='fixed',margin=(0,0,95,0),css_classes=['table'])

            s=pn.Column(pn.pane.Markdown("## ■ 물질특성", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),materials2_table,mark3,pn.pane.Markdown("<br>"),pn.pane.Markdown("## ■ Kma : 재질-공기 분배계수", style={'font-family': 'NanumBarunGothic','font-size':'15px'}),kmas2_table,pn.pane.Markdown("<br>"),pn.pane.Markdown("## ■ 제품중 농도", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pro_density_table,width=400,height=600,margin=(0,10,0,0))

            tabulator_editors3 = {
                '시나리오명': None,
                '분배비율':None,
                '시나리오구성':None,
            }

            scenario_ratio1=pd.DataFrame({'시나리오명':['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','합'],
            '분배비율':[text_input20.value,text_input21.value,text_input22.value,text_input23.value,text_input24.value,text_input25.value,text_input26.value,text_input27.value,text_input28.value,'1'],
            '시나리오구성':['바닥재(PVC floor), 종이벽지, 의자(mdf), 선반(mdf)','바닥재(PVC tile), 종이벽지, 의자(mdf), 선반(mdf)','바닥재(강화마루), 종이벽지, 의자(mdf), 선반(mdf)',
            '바닥재(PVC floor), 실크벽지, 의자(mdf), 선반(mdf) ','바닥재(PVC tile), 실크벽지, 의자(mdf), 선반(mdf)','바닥재(강화마루), 실크벽지, 의자(mdf), 선반(mdf)',
            '바닥재(PVC floor), paint, 의자(mdf), 선반(mdf)','바닥재(PVC tile), paint, 의자(mdf), 선반(mdf)','바닥재(강화마루), paint, 의자(mdf), 선반(mdf)','']})
            scenario_ratio1=scenario_ratio1.style.hide_index()
            scenario_ratio1_table=pn.widgets.Tabulator(scenario_ratio1,header_align='center',text_align='center',show_index=False,editors=tabulator_editors3,pagination='remote',sizing_mode='fixed',margin=(0,0,95,50),css_classes=['table'])

            scenario_ratio2=pd.DataFrame({'시나리오명':['가정집1','가정집2','가정집3','가정집4','합'],
            '분배비율':[text_input29.value,text_input30.value,text_input31.value,text_input32.value,'1'],
            '시나리오구성':['바닥재(PVC floor), 실크벽지, 신발장 1개, 책상 1개, 의자1개, 서랍 1개, 침대1,  부엌가구, 식탁, 의자2, 전자제품(나연제,voc)',
            '바닥재(강화마루), 종이벽지, 신발장 1개, 책상 1개, 의자1개, 서랍 2개, 침대2,  부엌가구2, 식탁, 의자4, 전자제품(나연제,voc)',
            '바닥재(PVC floor), 종이벽지, 신발장 1개, 책상 1개, 의자1개, 서랍 1개, 침대1,  부엌가구, 식탁, 의자2, 전자제품(나연제,voc)',
            '바닥재(강화마루), 실크벽지, 신발장 1개, 책상 1개, 의자1개, 서랍 2개, 침대2,  부엌가구2, 식탁, 의자4, 전자제품(나연제,voc)','']})
            scenario_ratio2=scenario_ratio2.style.hide_index()
            scenario_ratio2_table=pn.widgets.Tabulator(scenario_ratio2,header_align='center',text_align='center',show_index=False,editors=tabulator_editors3,pagination='remote',sizing_mode='fixed',width=1200,margin=(0,0,95,50),css_classes=['table'])

            scenario_ratio3=pd.DataFrame({'시나리오명':['학교1','학교2','합'],
            '분배비율':[text_input33.value,text_input34.value,'1'],
            '시나리오구성':['바닥재:PVC tile, 벽:페인트, 학생용책상(mdf) 24개, 의자 (mdf) 24개, 사물함 (mdf) 24개',
            '바닥재:나무, 벽:페인트, 학생용책상(mdf) 24개, 의자 (mdf) 24개, 사물함(mdf)24개',
            '']})
            scenario_ratio3=scenario_ratio3.style.hide_index()
            scenario_ratio3_table=pn.widgets.Tabulator(scenario_ratio3,header_align='center',text_align='center',show_index=False,editors=tabulator_editors3,pagination='remote',sizing_mode='fixed',margin=(0,0,95,50),css_classes=['table'])

            scenario_ratio4=pd.DataFrame({'시나리오명':['직장'],
            '분배비율':[text_input35.value],
            '시나리오구성':['바닥재(PVC tile), 사무용책상 10개, 의자 10개, 컴퓨터 10개']})
            scenario_ratio4=scenario_ratio4.style.hide_index()
            scenario_ratio4_table=pn.widgets.Tabulator(scenario_ratio4,header_align='center',text_align='center',show_index=False,editors=tabulator_editors3,pagination='remote',sizing_mode='fixed',margin=(0,0,95,50),css_classes=['table'])

            t=pn.Column(pn.pane.Markdown("## ■ 시나리오 분배비율 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.Markdown("### 활동공간-어린이집<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),scenario_ratio1_table,pn.pane.Markdown("### <br> 활동공간-일반가정집<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),scenario_ratio2_table,pn.pane.Markdown("### <br> 활동공간-학교<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),scenario_ratio3_table,pn.pane.Markdown("### <br> 활동공간-직장<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),scenario_ratio4_table,width=600,height=1200,margin=(0,0,0,220))

            flow_1=pn.Column(pn.pane.Markdown("## ■ 생활환경 유래 노출량 산정 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.JPG('그림1_수정.jpg',height=432,width=1098,margin=(0,0,50,0)),pn.pane.Markdown("## <br> ■ 생활환경 유래 노출량 산정 알고리즘 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.JPG('그림2_수정.jpg',height=406,width=1098,margin=(0,0,50,0)),mark2)
            # pn.Row(s,t)
            mark4=pn.pane.Markdown("## <br> ■ 전체 인구 기준 (n=20910) <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'})
            flow_2=pn.Column(mark2,pn.pane.JPG('방출모델_플로우차트.jpg',height=961,width=831,margin=(0,350,0,200)),mark2)

            def weight_plot(x,y,z):
                x1=list(x)
                hist_data = [x1]
                group_labels = [y]
                colors = ['#333F44']

                fig = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False, colors=colors)
                fig.update_xaxes(title=z)
                fig.update_yaxes(title="상대빈도(-)")
                fig.update_layout(title_text=y,width=600,height=600,showlegend=False)
                return fig
            # def weight_plot_page():
            wx='집에 머무는 시간 (min)'
            wy='주중 집에 24시간 중 머무는 시간'

            wx1='학교, 직장에 머무는 시간 (min)'
            wy1='주중 학교, 직장에 24시간 중 머무는 시간'

            wx2='주말 집에 머무는 시간 (min)'
            wy2='주말 집에 24시간 중 머무는 시간'

            wx3='체중 (kg)'
            wy3='체중 (kg)'

            # wx4='먼지 섭취량 (mg/day)'
            # wy4='먼지 섭취량 (mg/day)'

            # wx5='호흡률 (m³/day)'
            # wy5='호흡률 (m³/day)'
                # return pn.Column(pn.Row(weight_plot(np_data1[:,13],wy,wx),weight_plot((np_data1[:,14] + np_data1[:,15]),wy1,wx1),weight_plot(np_data1[:,16]),wy2,wx2),pn.Row(weight_plot(np_data1[:,19],wy3,wx3),weight_plot(np_data1[:,20],wy4,wx4),weight_plot(np_data1[:,21],wy5,wx5)))
            
            
#distplot이 필요한거는
# BW = np_data1[:,19] #체중
# np_data1[:,13] #주중 집에 24시간 중 머무는 시간 
# (np_data1[:,14] + np_data1[:,15])# 주중 학교, 직장에 24시간 중 머무는 시간 
# h_w_time_ratio = np_data1[:,16] # 주말 집에 24시간 중 머무는 시간 

# igR = np_data1[:,20] # 먼지 섭취량
# iR = np_data1[:,21] # 호흡률             
            age_gp = np.concatenate((np.repeat(1, len(idx1_mean)),
            np.repeat(2, len(idx2_mean)),
            np.repeat(3, len(idx3_mean)),
            np.repeat(4, len(idx4_mean)),
            np.repeat(5, len(idx5_mean))) )

            concat_exposure = np.concatenate((idx1_mean, idx2_mean, idx3_mean, idx4_mean, idx5_mean))

            exposure_df = pd.DataFrame({'age': age_gp, 'exposure':concat_exposure})

            IR_mean_df = pd.DataFrame({'age' : data['연령코드'] ,'IR' : np.mean(IR_array, axis = 1)})
            IR_mean_df = IR_mean_df.sort_values(by = 'age')

            #fig = px.box(IR_mean_df ,x='age', y="IR", color='age')
            
            def box_plot_Ir(x):
                fig = px.box(x ,x="age", y="IR", color="age")
                fig.update_xaxes(title="나이 (세)")
                fig.update_yaxes(title="호흡률 (m³/day)")
                fig.update_layout(title_text="호흡률 (m³/day)",width=600,height=600,showlegend=False)                
                return fig

            def plot_his(x):
                result_df=x
                fig = px.histogram(result_df, x=result_df[result_df['age'] == 1]['exposure'], title='10대 노출량',nbins=100)
                fig.update_layout(width=800,height=400)
                fig.update_xaxes(title="노출량 (ng/kg/day)")
                fig.update_yaxes(title="빈도")
                fig2 = px.histogram(result_df, x=result_df[result_df['age'] == 2]['exposure'], title='20대 노출량',nbins=100)
                fig2.update_layout(width=800,height=400)
                fig2.update_xaxes(title="노출량 (ng/kg/day)")
                fig2.update_yaxes(title="빈도")
                fig3 = px.histogram(result_df, x=result_df[result_df['age'] == 3]['exposure'], title='30대 노출량',nbins=100)
                fig3.update_layout(width=800,height=400)
                fig3.update_xaxes(title="노출량 (ng/kg/day)")
                fig3.update_yaxes(title="빈도")
                fig4 = px.histogram(result_df, x=result_df[result_df['age'] == 4]['exposure'], title='40대 노출량',nbins=100)
                fig4.update_layout(width=800,height=400)
                fig4.update_xaxes(title="노출량 (ng/kg/day)")
                fig4.update_yaxes(title="빈도")
                fig5 = px.histogram(result_df, x=result_df[result_df['age'] == 5]['exposure'], title='50대 노출량',nbins=100)
                fig5.update_layout(width=800,height=400)
                fig5.update_xaxes(title="노출량 (ng/kg/day)")
                fig5.update_yaxes(title="빈도")
                fig6 = px.histogram(result_df, x=result_df['exposure'], title='전체 노출량',nbins=100)
                fig6.update_layout(width=800,height=400)
                fig6.update_xaxes(title="노출량 (ng/kg/day)")
                fig6.update_yaxes(title="빈도")
                return pn.Column(fig,fig2,fig3,fig4,fig5,fig6)

            
            mark5=pn.pane.Markdown("## <br> ■ 개인 단위 간접 노출량 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}) 
            mark6=pn.pane.Markdown("## <br> ■ 연령별 개인단위 간접 노출량 히스토그램 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'})

            dust_ingestion_df = pd.DataFrame({'나이 (세)' : ['6주~1세','1세~6세','3세~6세','6세~21세','21세이상 어른'] ,'먼지 섭취량 (mg/day)' : [30,50,50,50,20]})
            tabulator_editors_di = {
                '나이 (세)': None,
                '먼지 섭취량 (mg/day)': None
            }
            dust_ingestion_mark=pn.pane.Markdown("### 먼지 섭취량 (mg/day) <br> ", style={'font-family': 'NanumBarunGothic','font-size':'15px'})
            dust_ingestion_table=pn.Column(dust_ingestion_mark,pn.widgets.Tabulator(dust_ingestion_df,header_align='center',text_align='center',editors=tabulator_editors_di,show_index=False,pagination='remote',sizing_mode='fixed',margin=(0,10,15,20),css_classes=['table']))        

            @pn.depends(x=radio_group3.param.value)
            def main_s(x):            
                if x =='공간별 노출매체 농도 예측 입력정보':
                    tab=pn.Column(flow_2,pn.Row(s,t))
                elif x =='공간별 노출매체 농도 예측결과':
                    tab=pn.Column(table2,pn.Row(fig2,fig3))
                elif x =='개인단위 간접 노출량 입력정보':
                    tab= pn.Column(flow_1,mark4,pn.Row(weight_plot(np_data1[:,13],wy,wx),weight_plot((np_data1[:,14] + np_data1[:,15]),wy1,wx1)),
                                                pn.Row(weight_plot(np_data1[:,16],wy2,wx2),weight_plot(np_data1[:,17],wy3,wx3)),
                                                pn.Row(dust_ingestion_table,box_plot_Ir(IR_mean_df)))
                elif x =='개인 단위 간접 노출량':
                    tab=pn.Column(mark5,pn.Row(line_fig(result_df,result_max_df,result_min_df),table_x),mark6,plot_his(exposure_df))
                return pn.Column(radio_group3,tab)
            tabs=pn.Column(main_s)
            tabs.background="#ffffff"

 ##############################################################           
        elif radio_group.value=='간접노출' and radio_group2.value=='휘발성 물질 (VOCs)':
            chemical = chemi_input.value #'화학물질0'
            pd.set_option('display.float_format', '{:.2e}'.format)
            #%% real data 
            furniture=  pd.read_csv( '가구 방출량.csv',  encoding = 'cp949',index_col = 0).T
            furniture_sc=  pd.read_csv('가구시나리오_new.csv',  encoding = 'cp949',index_col = 0).fillna(0)
            tile = pd.read_csv( '마감재 방출량_final.csv',  encoding = 'cp949',index_col = 0).T
            tile_sc =  pd.read_csv( '마감재 시나리오.csv',  encoding = 'cp949',index_col = 0).fillna(0)
            Q =  pd.read_csv('VOC_Q.csv', encoding = 'cp949')
            furniture = furniture.drop(labels = '물질명', axis =0)
            tile = tile.drop(labels = '물질명', axis =0)
            scenario_list =furniture_sc.columns

            def cons(x):
                a = furniture_sc[x] , tile_sc[x]
                b = furniture[chemical], tile[chemical]
                c =(b[0].dot(a[0]) +  b[1].dot(a[1]))/Q[x]
                return c
            vocs =  pd.concat(map(cons,scenario_list), axis =1, keys = scenario_list)
            vocs.index =[chemical]
            vocs=vocs.T

            vocs.rename(columns={chemical:'예측된 공기 농도 (㎍/㎥)'},inplace = True)
            vocs=vocs.transpose()
            vocs.columns=['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','가정집1','가정집2','가정집3','가정집4','학교1','학교2','직장']
            vocs=vocs.transpose()
            vocs2=vocs.copy()
            vocs2['공간별 시나리오'] = vocs2.index
            vocs2.index = range(len(vocs))
            vocs2 = vocs2[['공간별 시나리오', '예측된 공기 농도 (㎍/㎥)']]
            vocs2 = vocs2.style.hide_index()
            tabulator_editors = {
                '공간별 시나리오': None,
                '예측된 공기 농도 (㎍/㎥)':None,
            }
            vocs2_table=pn.widgets.Tabulator(vocs2,show_index=False,header_align='center',text_align='center',editors=tabulator_editors,pagination='remote',sizing_mode='fixed',margin=(0,0,55,0),css_classes=['table'])
            table2=pn.Column(pn.pane.Markdown("## ■ VOCs 시나리오별 실내환경매체 물질 농도 예측 <br> ", style={'font-family': 'NanumBarunGothic','font-size':'20px'},width=650,margin=(0, 75, 0, 0)),vocs2_table)

####  2번째탭 bar그래프 - air
            y3=pd.read_csv('voc_air.csv',index_col=0)
            if(y3.index==chemical).any():
                y2=vocs.copy()
                y2=y2.transpose()
                y2.columns=['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','가정집1','가정집2','가정집3','가정집4','학교1','학교2','직장']
                y2=y2.transpose()
                y3=pd.read_csv('voc_air.csv',index_col=0)
                y3.loc[[chemical]]

                fig2 = go.Figure(
                    data=[
                        go.Bar(
                            name="예측농도",
                            x=y2.index,
                            y=y2['예측된 공기 농도 (㎍/㎥)'],
                            offsetgroup=0,
                        ),
                        go.Bar(
                            name="실측농도",
                            x=y3["시설"],
                            y=y3["농도"],
                            offsetgroup=1,
                        ),
                    ],
                    layout=go.Layout(
                        title="VOCs 시나리오별 예측 공기 중 물질농도와 실측 공기 중 물질농도 비교 ("+chemical+")",
                        yaxis_title="예측된 공기 농도 (㎍/㎥)",
                        width=800, 
                        height=400,
                    )
                )
                fig2.update_yaxes(type='log')

            else:
                y2=vocs.copy()
                y2=y2.transpose()
                y2.columns=['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','가정집1','가정집2','가정집3','가정집4','학교1','학교2','직장']
                y2=y2.transpose()
                fig2 = px.bar(y2,x=y2.index, y='예측된 공기 농도 (㎍/㎥)')
                fig2.update_yaxes(type='log')
                fig2.update_layout(width=800, height=400,title="VOCs 시나리오별 예측 공기 중 물질농도와 실측 공기 중 물질농도 비교 ("+chemical+")")

            other_c_air = vocs.iloc[[0,1,2,3,4,5,6,7,8,13,14,15],:]
            other_c_air=other_c_air.T
            other_c_air.columns=['kinder_1','kinder_2','kinder_3','kinder_4','kinder_5','kinder_6','kinder_7','kinder_8','kinder_9','school_1','school_2','work_1']
            other_c_air=other_c_air.T
            home_c_air = vocs.iloc[9:13,:]
            home_c_air=home_c_air.T
            home_c_air.columns=['home_1','home_2','home_3','home_4']
            home_c_air=home_c_air.T
            # other_c_dust = y_dust.iloc[[0,1,2,3,4,5,6,7,8,13,14,15],:]
            # home_c_dust = y_dust.iloc[9:13,:]
            data = pd.read_csv('NF_scenario_new.csv', encoding='cp949') 

            def bw_function(x,y):
                x = int(x)
                y = str(y)

                if (10 <= x <= 12) & (y == '남자'):
                    return np.random.normal(44.7 ,10.92,100)
                elif (13 <= x <= 15) & (y == '남자'):
                    return np.random.normal(61.5 ,13.66,100)
                elif (16 <= x <= 18) & (y == '남자'):
                    return np.random.normal(67.3 ,13.97,100)
                elif (19 <= x <= 24) & (y == '남자'):
                    return np.random.normal(70.7 ,12.60,100)
                elif (25 <= x <= 34) & (y == '남자'):
                    return np.random.normal(75.6 ,12.72,100)
                elif (35 <= x <= 44) & (y == '남자'):
                    return np.random.normal(75.2 ,11.84,100)
                elif (45 <= x <= 54) & (y == '남자'):
                    return np.random.normal(71.4 ,10.10,100)
                elif (55 <= x <= 64) & (y == '남자'):
                    return np.random.normal(68.6 ,9.55,100)
                elif (65 <= x <= 74) & (y == '남자'):
                    return np.random.normal(65.6 ,9.33,100)
                elif (75 <= x) & (y == '남자'):
                    return np.random.normal(61.7 ,9.01,100)

                elif (10 <= x <= 12) & (y == '여자'):
                    return np.random.normal(42.7 ,9.95,100)
                elif (13 <= x <= 15) & (y == '여자'):
                    return np.random.normal(52.8 ,9.74,100)
                elif (16 <= x <= 18) & (y == '여자'):
                    return np.random.normal(56.8 ,9.80,100)
                elif (19 <= x <= 24) & (y == '여자'):
                    return np.random.normal(56.0 ,9.77,100)
                elif (25 <= x <= 34) & (y == '여자'):
                    return np.random.normal(57.7 ,10.54,100)
                elif (35 <= x <= 44) & (y == '여자'):
                    return np.random.normal(58.5 ,9.58,100)
                elif (45 <= x <= 54) & (y == '여자'):
                    return np.random.normal(59.0 ,8.69,100)
                elif (55 <= x <= 64) & (y == '여자'):
                    return np.random.normal(58.4 ,8.53,100)
                elif (65 <= x <= 74) & (y == '여자'):
                    return np.random.normal(57.6 ,8.32,100)
                elif (75 <= x) & (y == '여자'):
                    return np.random.normal(53.4 ,9.02,100)

            bw_df = data.apply(lambda x: bw_function(x['연령'], x['성별코드']), axis=1)
            bw_df = pd.DataFrame(bw_df, columns =['bw'])


            bw_df = pd.DataFrame(bw_df['bw'].values.tolist()).add_prefix('iteration')#.join(c)
            BW_array = np.array(bw_df)
            BW_array[BW_array < 0] = 1

            def IR_function(x):
                if x == 10:
                    return np.random.normal(12.23,1.06,100)
                elif x == 11:
                    return np.random.normal(12.51,0.61,100)
                elif x == 12:
                    return np.random.normal(13.36,1.01,100)
                elif x == 13:
                    return np.random.normal(13.97,1.55,100)
                elif x == 14:
                    return np.random.normal(14.55,2.33,100)
                elif x == 15:
                    return np.random.normal(14.61,1.43,100)
                elif x == 16:
                    return np.random.normal(15.16,1.94,100)
                elif x == 17:
                    return np.random.normal(14.26,1.31,100)
                elif x == 18:
                    return np.random.normal(15.76,2.23,100)
                elif 19 <= x <= 24:
                    return np.random.normal(13.09,3.17,100)
                elif 25 <= x <= 34:
                    return np.random.normal(14.53,3,100)
                elif 35 <= x <= 44:
                    return np.random.normal(15.96,3.17,100)
                elif 45 <= x <= 54:
                    return np.random.normal(14.62,3.32,100)
                else:
                    return np.random.normal(14.79,2.71,100)

            IR_df = data['연령'].apply(IR_function)
            IR_df = pd.DataFrame(IR_df)


            IR_df = pd.DataFrame(IR_df['연령'].values.tolist()).add_prefix('iteration')#.join(c)
            IR_array = np.array(IR_df)
            IR_array[IR_array < 0] = 0

            # 시나리오 부여

            # 어린이(13세 미만), 청소년 및 성인 따로 분류
            data_child = data[data.연령 < 13]
            data_other_work = data[(data.연령 > 12) & ((data.work_daily > 0) | (data.school_daily > 0))]
            data_other_home = data[(data.연령 > 12) & ((data.work_daily == 0) & (data.school_daily == 0))]

            # 학교 시나리오 분배를 위한 분배비율 default, 사용자가 수정할 경우 그 입력값을 prob로 받아옴
            prob = {'school_1': float(text_input33.value),
                    'school_2': float(text_input34.value),
                    } 

            # 어린이의 학교 시나리오 분배, 청소년 및 성인의 other (직장 또는 학교) 시나리오 분배, 직장을 다니지 않는 성인의 시나리오 0 분배

            data_child.loc[:,'other_sn'] = np.random.choice(list(prob.keys()), size=len(data_child), replace = True, p=list(prob.values()))
            data_other_work.loc[:,'other_sn'] = 'work_1'
            data_other_home.loc[:, 'other_sn'] = 0

            data_1 = pd.concat([data_child, data_other_work, data_other_home], ignore_index=True)
            data_1 = data_1.sort_values(by=['가구일련번호', '가구원일련번호'])

            # 가정 시나리오 분배를 위한 분배비율 default, 사용자가 수정할 경우 그 입력값을 prob_1로 받아옴
            prob_1 = {'home_1': float(text_input29.value),
                    'home_2': float(text_input30.value),
                    'home_3': float(text_input31.value),
                    'home_4': float(text_input32.value)}
            # 가구별 home_i 시나리오 분배
            data_2 = data_1.groupby(['가구일련번호'], as_index=False).size()
            data_2.loc[:, 'home_sn'] = np.random.choice(list(prob_1.keys()), size=len(data_2), replace = True, p=list(prob_1.values()))
            data_2 = data_2.drop(columns='size')

            # 가구별 home 시나리오를 개인별 데이터(data_1)과 합치고 data_3로 통합
            data_3 = pd.merge(data_1, data_2, left_on='가구일련번호', right_on='가구일련번호', how='left')


            # 활동공간별 농도값을 data 테이블에 합침

            data_4 = pd.merge(data_3, other_c_air, left_on='other_sn', right_on=other_c_air.index, how='left')
            data_4 = pd.merge(data_4, home_c_air, left_on='home_sn', right_on=home_c_air.index, how='left')
            # data_4 = pd.merge(data_4, other_c_dust, left_on='other_sn', right_on=other_c_dust.index, how='left')
            # data_4 = pd.merge(data_4, home_c_dust, left_on='home_sn', right_on=home_c_dust.index, how='left')
            data_4.info()
            data_4 = data_4.fillna(0) # NAN이 있는 경우 노출량 계산결과가 NAN으로 나오므로, NAN을 0값으로 대체


            np_data1 = data_4.to_numpy() # 쉬운 계산을 위하여 numpy array로 변경


            # 노출계수 정의
            h_c_air = np_data1[:,23].reshape(len(np_data1),1)  #집 공기중 농도
            o_c_air = np_data1[:,22].reshape(len(np_data1),1)  #학교, 직장 공기 중 농도
            # h_c_dust = np_data1[:,25].reshape(len(np_data1),1) #집 먼지 중 농도
            # o_c_dust = np_data1[:,24].reshape(len(np_data1),1) #학교, 직장 먼지 중 농도

            #BW = np_data1[:,17].reshape(len(np_data1),1) #체중
            h_d_time_ratio = (np_data1[:,13]/1440).reshape(len(np_data1),1) #주중 집에 24시간 중 머무는 시간 비율
            o_d_time_ratio = ( (np_data1[:,14] + np_data1[:,15])/1440 ).reshape(len(np_data1),1) # 주중 학교, 직장에 24시간 중 머무는 시간 비율
            h_w_time_ratio = ( np_data1[:,16]/1440 ).reshape(len(np_data1),1) # 주말 집에 24시간 중 머무는 시간 비율

            # igR = np_data1[:,18].reshape(len(np_data1),1) # 먼지 섭취량


            # air exposure = conc * IR * AR / BW,                 air conc = conc * AR
            # dust exposure = conc * dust_IgR * AR / BW

            exp_inh_air_home_daily = h_c_air * IR_array * h_d_time_ratio / BW_array # 주중 집에 머무는 시간에 대한 실내공기 노출량
            exp_inh_air_other_daily = o_c_air * IR_array * o_d_time_ratio / BW_array # 주중 활동공간에 머무는 시간에 대한 실내공기 노출량
            exp_inh_air_home_weekend = h_c_air * IR_array * h_w_time_ratio / BW_array # 주말 집에 머무는 시간에 대한 실내공기 노출량

            #exp_inh_air_home_daily_sorted = np.sort(exp_inh_air_home_daily, axis=0)
            #exp_inh_air_other_daily_sorted = np.sort(exp_inh_air_other_daily, axis=0)
            #exp_inh_air_home_weekend_sorted = np.sort(exp_inh_air_home_weekend, axis=0)

            #np.min(exp_inh_air_home_daily_sorted, axis = 1)


            # exp_inh_dust_home_daily = h_c_dust * igR * h_d_time_ratio / BW_array # 주중 집에 머무는 시간에 대한 먼지 노출량
            # exp_inh_dust_other_daily = o_c_dust * igR * o_d_time_ratio / BW_array # 주중 활동공간에 머무는 시간에 대한 먼지 노출량
            # exp_inh_dust_home_weekend = h_c_dust * igR * h_w_time_ratio / BW_array # 주말 집에 머무는 시간에 대한 먼지 노출량


            # air_conc = conc * AR : 노출량(mg/kg-day)이 아닌 노출농도 계산(mg/m3)
            conc_inh_air_home_daily = h_c_air * h_d_time_ratio # 주중 집에 머무는 시간에 대한 실내공기 노출농도
            conc_inh_air_other_daily = o_c_air * o_d_time_ratio # 주중 활동공간에 머무는 시간에 대한 실내공기 노출농도
            conc_inh_air_home_weekend = h_c_air * h_w_time_ratio # 주말 집에 머무는 시간에 대한 실내공기 노출농도


            #일주일 평균 노출량 >> (5* daily exposure(home+other) + 2*weekend exposure )/7
            mean_exp_air = ( 5*(exp_inh_air_home_daily + exp_inh_air_other_daily) + (2*exp_inh_air_home_weekend))/7 # 일주일 실내공기 평균 노출량

            # 일주일 평균 노출농도 >> (5* daily exposure(home+other) + 2*weekend exposure )/7
            mean_conc_air = ( 5*(conc_inh_air_home_daily + conc_inh_air_other_daily) + (2*conc_inh_air_home_weekend))/7 # 일주일 실내공기 평균 노출농도


            # mean_exp_dust = ( 5*(exp_inh_dust_home_daily + exp_inh_dust_other_daily) + (2*exp_inh_dust_home_weekend))/7 # 일주일 평균 먼지 노출량

            total_exp = mean_exp_air # 먼지 + 실내공기 통합 노출량
#######################################
            total_exp_sorted = np.sort(total_exp, axis=0)
            total_exp_sorted_idx = np.argsort(total_exp, axis=0)

            a = np.mean(total_exp_sorted, axis=1)
            a_min = np.min(total_exp_sorted, axis=1)
            a_max = np.max(total_exp_sorted, axis=1)

            total_exp_sorted_5th = total_exp_sorted[int((len(a) - 1) * 0.05),:]
            total_exp_sorted_50th = total_exp_sorted[int((len(a) - 1) * 0.5),:]
            total_exp_sorted_95th = total_exp_sorted[int((len(a) - 1) * 0.95),:]

            #calculate CDF values
            a_y = 1. * np.arange(len(a)) / (len(a) - 1)

            result_df = pd.DataFrame({'exp':a, 'cdf':a_y})
            result_df['chemi']=str(chemical)
            result_df.to_csv('indirect.csv')
            result_min_df = pd.DataFrame({'exp':a_min, 'cdf':a_y})
            result_max_df = pd.DataFrame({'exp':a_max, 'cdf':a_y})

            def line_fig(a,b,c):
                fig5 = go.Figure([
                    go.Scatter(
                        name='Mean',
                        x=a['exp'], #result_df
                        y=a['cdf'],
                        mode='lines',
                        line=dict(color='rgb(31, 119, 180)'),
                    ),
                    go.Scatter(
                        name='Upper Bound',
                        x=b['exp'], #result_max_df
                        y=b['cdf'],
                        mode='lines',
                        marker=dict(color="#444"),
                        line=dict(width=0),
                        showlegend=False
                    ),
                    go.Scatter(
                        name='Lower Bound',
                        x=c['exp'], #result_min_df
                        y=c['cdf'],
                        marker=dict(color="#444"),
                        line=dict(width=0),
                        mode='lines',
                        fillcolor='rgba(68, 68, 68, 0.3)',
                        fill='tonexty',
                        showlegend=False
                    )
                ])

                fig5.update_layout(
                    xaxis_title='노출량 (ng/kg/day)',
                    yaxis_title='CDF',
                    title='노출량 (ng/kg/day)',
                    hovermode="x",
                    width=850,
                    height=550,
                )
                fig5.update_layout(xaxis_type="log")
                return pn.Column(fig5,sizing_mode='fixed',margin=(0,100,0,0))

##### 마지막탭 내용
            idx1 = list(data_4[(10 <= data_4['연령']) & (data_4['연령'] <= 19)].index)
            idx2 = list(data_4[(20 <= data_4['연령']) & (data_4['연령'] <= 29)].index)
            idx3 = list(data_4[(30 <= data_4['연령']) & (data_4['연령'] <= 39)].index)
            idx4 = list(data_4[(40 <= data_4['연령']) & (data_4['연령'] <= 49)].index)
            idx5 = list(data_4[50 <= data_4['연령']].index)

            idx1_mean = np.mean(total_exp[idx1,:], axis=1)
            idx2_mean = np.mean(total_exp[idx2,:], axis=1)
            idx3_mean = np.mean(total_exp[idx3,:], axis=1)
            idx4_mean = np.mean(total_exp[idx4,:], axis=1)
            idx5_mean = np.mean(total_exp[idx5,:], axis=1)

            idx1_500_mean = np.mean(total_exp[idx1,:], axis=0)
            idx2_500_mean = np.mean(total_exp[idx2,:], axis=0)
            idx3_500_mean = np.mean(total_exp[idx3,:], axis=0)
            idx4_500_mean = np.mean(total_exp[idx4,:], axis=0)
            idx5_500_mean = np.mean(total_exp[idx5,:], axis=0)

            def exp_table(mu,std):
                return str(format(mu,'.2E')) + "(±" + str(format(std,'.2E')) + ")"

                
            idx1_min = idx1_500_mean.min()

            v1 = exp_table(idx1_500_mean.mean(), np.std(idx1_500_mean))
            v2 = exp_table(idx2_500_mean.mean(), np.std(idx2_500_mean))
            v3 = exp_table(idx3_500_mean.mean(), np.std(idx3_500_mean))
            v4 = exp_table(idx4_500_mean.mean(), np.std(idx4_500_mean))
            v5 = exp_table(idx5_500_mean.mean(), np.std(idx5_500_mean))

            age_list = ['10대', '20대', '30대', '40대', '50대 이상']

            exposure_table = pd.DataFrame({'연령': age_list,'노출량 (ng/kg/day)': [v1,v2,v3,v4,v5]})
            exposure_table=exposure_table.style.hide_index()
            tabulator_editors2 = {
                '연령': None,
                '노출량 (ng/kg/day)':None
            }
            table_x=pn.widgets.Tabulator(exposure_table,show_index=False,header_align='center',text_align='center',editors=tabulator_editors2,pagination='remote',sizing_mode='fixed',margin=(150,0,25,0),css_classes=['table'])
#######################################
#입력정보
#######################################
            tabulator_editors3 = {
                '시나리오명': None,
                '분배비율':None,
                '시나리오구성':None,
            }

            scenario_ratio1=pd.DataFrame({'시나리오명':['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9','합'],
            '분배비율':[text_input20.value,text_input21.value,text_input22.value,text_input23.value,text_input24.value,text_input25.value,text_input26.value,text_input27.value,text_input28.value,'1'],
            '시나리오구성':['바닥재(PVC floor), 종이벽지, 의자, 선반','바닥재(PVC tile), 종이벽지, 의자, 선반','바닥재(강화마루), 종이벽지, 의자, 선반',
            '바닥재(PVC floor), 실크벽지, 의자, 선반 ','바닥재(PVC tile), 실크벽지, 의자, 선반','바닥재(강화마루), 실크벽지, 의자, 선반',
            '바닥재(PVC floor), paint, 의자, 선반','바닥재(PVC tile), paint, 의자, 선반','바닥재(강화마루), paint, 의자, 선반','']})
            scenario_ratio1=scenario_ratio1.style.hide_index()
            scenario_ratio1_table=pn.widgets.Tabulator(scenario_ratio1,header_align='center',text_align='center',show_index=False,editors=tabulator_editors3,pagination='remote',sizing_mode='fixed',margin=(0,0,95,50),css_classes=['table'])

            scenario_ratio2=pd.DataFrame({'시나리오명':['가정집1','가정집2','가정집3','가정집4','합'],
            '분배비율':[text_input29.value,text_input30.value,text_input31.value,text_input32.value,'1'],
            '시나리오구성':['바닥재(PVC floor), 실크벽지, 신발장 1개, 책상 1개, 의자1개, 서랍 1개, 침대1,  부엌가구, 식탁, 의자2, 전자제품',
            '바닥재(강화마루), 종이벽지, 신발장 1개, 책상 1개, 의자1개, 서랍 1개, 침대2,  부엌가구1, 식탁, 의자2, 전자제품',
            '바닥재(PVC floor), 종이벽지, 신발장 1개, 책상 1개, 의자1개, 서랍 1개, 침대1,  부엌가구1, 식탁, 의자2, 전자제품',
            '바닥재(강화마루), 실크벽지, 신발장 1개, 책상 1개, 의자1개, 서랍 1개, 침대2,  부엌가구1, 식탁, 의자2, 전자제품','']})
            scenario_ratio2=scenario_ratio2.style.hide_index()
            scenario_ratio2_table=pn.widgets.Tabulator(scenario_ratio2,header_align='center',text_align='center',show_index=False,editors=tabulator_editors3,pagination='remote',sizing_mode='fixed',width=1000,margin=(0,0,95,50),css_classes=['table'])

            scenario_ratio3=pd.DataFrame({'시나리오명':['학교1','학교2','합'],
            '분배비율':[text_input33.value,text_input34.value,'1'],
            '시나리오구성':['바닥재:PVC tile, 벽:페인트, 학생용책상 24개, 의자 24개, 사물함 6개',
            '바닥재:나무, 벽:페인트, 학생용책상 24개, 의자  24개, 사물함6개','']})
            scenario_ratio3=scenario_ratio3.style.hide_index()
            scenario_ratio3_table=pn.widgets.Tabulator(scenario_ratio3,header_align='center',text_align='center',show_index=False,editors=tabulator_editors3,pagination='remote',sizing_mode='fixed',margin=(0,0,95,50),css_classes=['table'])

            scenario_ratio4=pd.DataFrame({'시나리오명':['직장'],
            '분배비율':[text_input35.value],
            '시나리오구성':['바닥재(PVC tile), 사무용책상 10개, 의자 10개, 컴퓨터 10개']})
            scenario_ratio4=scenario_ratio4.style.hide_index()
            scenario_ratio4_table=pn.widgets.Tabulator(scenario_ratio4,header_align='center',text_align='center',show_index=False,editors=tabulator_editors3,pagination='remote',sizing_mode='fixed',margin=(0,0,95,50),css_classes=['table'])

            t=pn.Column(pn.pane.Markdown("## ■ 시나리오 분배비율 (Default) <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.Markdown("### 활동공간-어린이집<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),scenario_ratio1_table,pn.pane.Markdown("### <br> 활동공간-일반 가정<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),scenario_ratio2_table,pn.pane.Markdown("### <br> 활동공간-학교<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),scenario_ratio3_table,pn.pane.Markdown("### <br> 활동공간-직장<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),scenario_ratio4_table,width=600,height=1200,margin=(0,0,0,220))

######################
            tabulator_editors4 = {
                '벽면적 (㎡)': None,
                '바닥면적 (㎡)':None,
                '환기량면적 (㎥/h)':None,
            }
            material_ratio1=pd.DataFrame({'시나리오명':['어린이집1','어린이집2','어린이집3','어린이집4','어린이집5','어린이집6','어린이집7','어린이집8','어린이집9'],
            '벽면적 (㎡)':['103','103','103','103','103','103','103','103','103'],
            '바닥면적 (㎡)':['361','361','361','361','361','361','361','361','361'],
            '환기량면적 (㎥/h)':['258','258','258','258','258','258','258','258','258']})
            material_ratio1=material_ratio1.style.hide_index()
            material_ratio1_table=pn.widgets.Tabulator(material_ratio1,header_align='center',text_align='center',show_index=False,editors=tabulator_editors4,pagination='remote',sizing_mode='fixed',margin=(0,0,95,0),css_classes=['table'])

            material_ratio2=pd.DataFrame({'시나리오명':['가정집1','가정집2','가정집3','가정집4'],
            '벽면적 (㎡)':['102','102','102','102'],
            '바닥면적 (㎡)':['356','356','356','356'],
            '환기량면적 (㎥/h)':['254','254','254','254']})
            material_ratio2=material_ratio2.style.hide_index()
            material_ratio2_table=pn.widgets.Tabulator(material_ratio2,header_align='center',text_align='center',show_index=False,editors=tabulator_editors4,pagination='remote',sizing_mode='fixed',margin=(0,0,95,0),css_classes=['table'])

            material_ratio3=pd.DataFrame({'시나리오명':['학교1','학교2'],
            '벽면적 (㎡)':['66','66'],
            '바닥면적 (㎡)':['231','231'],
            '환기량면적 (㎥/h)':['165','165']})
            material_ratio3=material_ratio3.style.hide_index()
            material_ratio3_table=pn.widgets.Tabulator(material_ratio3,header_align='center',text_align='center',show_index=False,editors=tabulator_editors4,pagination='remote',sizing_mode='fixed',margin=(0,0,95,0),css_classes=['table'])
            #85	298	213
            material_ratio4=pd.DataFrame({'시나리오명':['직장'],
            '벽면적 (㎡)':['85'],
            '바닥면적 (㎡)':['298'],
            '환기량면적 (㎥/h)':['213']})
            material_ratio4=material_ratio4.style.hide_index()
            material_ratio4_table=pn.widgets.Tabulator(material_ratio4,header_align='center',text_align='center',show_index=False,editors=tabulator_editors4,pagination='remote',sizing_mode='fixed',margin=(0,0,95,0),css_classes=['table'])

            www=pn.Column(pn.pane.Markdown("## ■ 시나리오 별 공간특성  <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.Markdown("### 활동공간-어린이집<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),material_ratio1_table,pn.pane.Markdown("### <br> 활동공간-일반 가정<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),material_ratio2_table,pn.pane.Markdown("### <br> 활동공간-학교<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),material_ratio3_table,pn.pane.Markdown("### <br> 활동공간-직장<br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),material_ratio4_table,width=600,height=1200,margin=(0,10,0,0))


            def weight_plot(x,y,z):
                x1=list(x)
                hist_data = [x1]
                group_labels = [y]
                colors = ['#333F44']

                fig = ff.create_distplot(hist_data, group_labels, show_hist=False, show_rug=False, colors=colors)
                fig.update_xaxes(title=z)
                fig.update_yaxes(title="상대빈도(-)")
                fig.update_layout(title_text=y,width=600,height=600,showlegend=False)
                return fig

            # def weight_plot_page():
            wx='집에 머무는 시간 (min)'
            wy='주중 집에 24시간 중 머무는 시간'

            wx1='학교, 직장에 머무는 시간 (min)'
            wy1='주중 학교, 직장에 24시간 중 머무는 시간'

            wx2='주말 집에 머무는 시간 (min)'
            wy2='주말 집에 24시간 중 머무는 시간'

            wx3='체중 (kg)'
            wy3='체중 (kg)'

            # wx4='먼지 섭취량 (mg/day)'
            # wy4='먼지 섭취량 (mg/day)'

            wx5='호흡률 (m³/day)'
            wy5='호흡률 (m³/day)'
####################################
            age_gp = np.concatenate((np.repeat(1, len(idx1_mean)),
            np.repeat(2, len(idx2_mean)),
            np.repeat(3, len(idx3_mean)),
            np.repeat(4, len(idx4_mean)),
            np.repeat(5, len(idx5_mean))) )

            concat_exposure = np.concatenate((idx1_mean, idx2_mean, idx3_mean, idx4_mean, idx5_mean))

            exposure_df = pd.DataFrame({'age': age_gp, 'exposure':concat_exposure})

            def plot_his(x):
                result_df=x
                fig = px.histogram(result_df, x=result_df[result_df['age'] == 1]['exposure'], title='10대 노출량',nbins=100)
                fig.update_layout(width=800,height=400)
                fig.update_xaxes(title="노출량 (ng/kg/day)")
                fig.update_yaxes(title="빈도")
                fig2 = px.histogram(result_df, x=result_df[result_df['age'] == 2]['exposure'], title='20대 노출량',nbins=100)
                fig2.update_layout(width=800,height=400)
                fig2.update_xaxes(title="노출량 (ng/kg/day)")
                fig2.update_yaxes(title="빈도")
                fig3 = px.histogram(result_df, x=result_df[result_df['age'] == 3]['exposure'], title='30대 노출량',nbins=100)
                fig3.update_layout(width=800,height=400)
                fig3.update_xaxes(title="노출량 (ng/kg/day)")
                fig3.update_yaxes(title="빈도")
                fig4 = px.histogram(result_df, x=result_df[result_df['age'] == 4]['exposure'], title='40대 노출량',nbins=100)
                fig4.update_layout(width=800,height=400)
                fig4.update_xaxes(title="노출량 (ng/kg/day)")
                fig4.update_yaxes(title="빈도")
                fig5 = px.histogram(result_df, x=result_df[result_df['age'] == 5]['exposure'], title='50대 노출량',nbins=100)
                fig5.update_layout(width=800,height=400)
                fig5.update_xaxes(title="노출량 (ng/kg/day)")
                fig5.update_yaxes(title="빈도")
                fig6 = px.histogram(result_df, x=result_df['exposure'], title='전체 노출량',nbins=100)
                fig6.update_layout(width=800,height=400)
                fig6.update_xaxes(title="노출량 (ng/kg/day)")
                fig6.update_yaxes(title="빈도")
                return pn.Column(fig,fig2,fig3,fig4,fig5,fig6)
###################################
            flow_1=pn.Column(pn.pane.Markdown("## ■ 생활환경 유래 노출량 산정 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.JPG('그림1_수정.jpg',height=432,width=1098,margin=(0,0,50,0)),pn.pane.Markdown("## <br> ■ 생활환경 유래 노출량 산정 알고리즘 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),pn.pane.JPG('그림2_수정.jpg',height=406,width=1098,margin=(0,0,50,0)),mark2)
            # pn.Row(s,t)
            flow_2=pn.Column(mark2,pn.pane.JPG('방출모델_플로우차트.jpg',height=961,width=831,margin=(0,350,0,200)),mark2)
            mark4=pn.pane.Markdown("## <br> ■ 전체 인구 기준 (n=20910) <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'})

            voc_kind=pd.DataFrame({'어린이집':[text_input36.value,text_input37.value,text_input59.value,text_input60.value,
                                                '0','0','0','0','0','0','0','0','0','0','0','0','0'],
                                    '일반 가정집':[text_input43.value,text_input42.value,text_input38.value,text_input39.value,
                                                    text_input40.value,text_input41.value,text_input45.value,text_input46.value,text_input47.value,
                                                        '0','0','0',text_input44.value,'0','0','0','0'],
                                    '학교':['0','0','0','0','0','0','0','0','0',text_input48.value,text_input49.value,text_input50.value,text_input51.value,
                                            '0','0','0','0'],
                                    '직장':['0','0','0','0','0','0','0','0','0','0','0','0','0',text_input52.value,text_input53.value,
                                            text_input54.value,text_input55.value]},index = ['가정용 의자', '서랍장','신발장','가정용 책상','침대',
                                            '부엌가구','프린터','청소기','냉장고','학교 책상','학교 사물함','학교 의자','TV','컴퓨터','모니터','사무용책상','사무용의자'])
            voc_kind=voc_kind.T
            tabulator_editors_voc = {
                '가정용 의자':None,
                '서랍장':None,
                '신발장':None,
                '가정용 책상':None,
                '침대':None,
                '부엌가구':None,
                '프린터':None,
                '청소기':None,
                '냉장고':None,
                '학교 책상':None,
                '학교 사물함':None,
                '학교 의자':None,
                'TV':None,
                '컴퓨터':None,
                '모니터':None,
                '사무용책상':None,
                '사무용의자':None,
            }
            voc_kind_tabulator=pn.widgets.Tabulator(voc_kind,header_align='center',text_align='center',show_index=False,editors=tabulator_editors_voc,pagination='remote',sizing_mode='fixed',margin=(0,0,55,0),css_classes=['table'])
            voc_kind_table=pn.Column(pn.pane.Markdown("## ■ 시나리오별 가구갯수 입력값 확인 <br> ", style={'font-family': 'NanumBarunGothic','font-size':'20px'}),voc_kind_tabulator,pn.pane.Markdown("<br>"),width=1000,height=400,margin=(0,10,0,0))
            mark5=pn.pane.Markdown("## <br> ■ 개인 단위 간접 노출량 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'})
            mark6=pn.pane.Markdown("## <br> ■ 연령별 개인단위 간접 노출량 히스토그램 <br>", style={'font-family': 'NanumBarunGothic','font-size':'20px'})

            IR_mean_df = pd.DataFrame({'age' : data['연령코드'] ,'IR' : np.mean(IR_array, axis = 1)})
            IR_mean_df = IR_mean_df.sort_values(by = 'age')

            #fig = px.box(IR_mean_df ,x='age', y="IR", color='age')
            
            def box_plot_Ir(x):
                fig = px.box(x ,x="age", y="IR", color="age")
                fig.update_xaxes(title="나이 (세)")
                fig.update_yaxes(title="호흡률 (m³/day)")
                fig.update_layout(title_text="호흡률 (m³/day)",width=600,height=600,showlegend=False)                
                return fig

            @pn.depends(x=radio_group4.param.value)
            def main_s(x):            
                if x =='공간별 노출매체 농도 예측 입력정보':
                    tab=pn.Column(flow_2,voc_kind_table,pn.Row(www,t))
                elif x =='공간별 노출매체 농도 예측결과':
                    tab=pn.Row(table2,fig2)
                elif x =='개인단위 간접 노출량 입력정보':
                    tab=pn.Column(flow_1,mark4,pn.Row(weight_plot(np_data1[:,13],wy,wx),weight_plot((np_data1[:,14] + np_data1[:,15]),wy1,wx1)),pn.Row(weight_plot(np_data1[:,16],wy2,wx2),weight_plot(np_data1[:,17],wy3,wx3)),box_plot_Ir(IR_mean_df))
                elif x =='개인 단위 간접 노출량':
                    tab=pn.Column(mark5,pn.Row(line_fig(result_df,result_max_df,result_min_df),table_x),mark6,plot_his(exposure_df))
                return pn.Column(radio_group4,tab)
            tabs=pn.Column(main_s)
            tabs.background="#ffffff"

        elif radio_group.value=='직접노출':
            alg_name, gen_alg1, gen_alg2, gen_alg3, gen_alg4, gen_alg5, gen_alg6,p2_table_data, p3_table_data, p4_table_data,\
            p6_table_data, p13, p14, p15, p16, data, p18, alg_sum, selected_product_list,p19,p20\
            = biocide.user_input(chemi_input.value, float(text_input56.value), float(text_input57.value), 1.0, 1.0)

            input_chemical=chemi_input.value
            M= float(text_input56.value)
            P_vap = float(text_input57.value)
            der_abs = 1.0
            inh_abs = 1.0

            product_content = pd.read_csv('product_chem_final.csv', encoding = 'CP949')
            alg_list = pd.read_csv('algo_final_ver.4(final).csv', encoding = 'CP949')

            def create_Exposure_intensity() :
                text = '## * 제품별 노출강도 (경피노출, 흡입노출)'
                def make_plot(title, ax, label):
                    if len(ax) != 0:
                        p = bokeh.plotting.figure(sizing_mode="fixed", width=800, height=600) #,x_axis_type="log"
                    else:
                        p = bokeh.plotting.figure(sizing_mode="fixed", width=800, height=600) #,x_axis_type="log"
                    p.xaxis.axis_label = label
                    p.title.text = str(title)
                    hist, edges = np.histogram(ax, density=True, bins=30)
                    p.quad(top=hist, bottom=0, color='#E69F00', alpha=0.3, left=edges[:-1], right=edges[1:])
                    p.xaxis[0].formatter = FuncTickFormatter(code="""
                                var str = tick.toString(); //get exponent
                                var newStr = "";
                                for (var i=0; i<10;i++)
                                {
                                    var code = str.charCodeAt(i);
                                    switch(code) {
                                    case 45: // "-"
                                        newStr += "⁻";
                                        break;
                                    case 48: // "0"
                                        newStr +="⁰";
                                        break;
                                    case 49: // "1"
                                        newStr +="¹";
                                        break;
                                    case 50: // "2"
                                        newStr +="²";
                                        break;
                                    case 51: // "3"
                                        newStr +="³"
                                        break;
                                    case 52: // "4"
                                        newStr +="⁴"
                                        break;
                                    case 53: // "5"
                                        newStr +="⁵"
                                        break;                
                                    case 54: // "6"
                                        newStr +="⁶"
                                        break;
                                    case 55: // "7"
                                        newStr +="⁷"
                                        break;
                                    case 56: // "8"
                                        newStr +="⁸"
                                        break;
                                    case 57: // "9"
                                        newStr +="⁹"
                                        break;                         
                                    }
                                }
                                return 10+newStr;
                                """)
                    p.axis.major_label_text_font = "sans"
                    return p

                column = bokeh.layouts.Column(
                    children=[_markdown(text)])
                for i in selected_product_list:
                    for j in alg_name.keys():
                        if alg_list[alg_list["code"] == i][j].values[0] == 1:
                            chart_title = alg_list[alg_list['code'] == i]['category'].values + ' ' + \
                                        alg_list[alg_list['code'] == i]['use'].values + ' ' + alg_list[alg_list['code'] == i][
                                            'type_1'].values + ' ' + alg_list[alg_list['code'] == i]['type_2'].values + ', ' + \
                                        alg_name[j] +' (노출강도)'
                            if j == 'airborne_short' :
                                label = 'mg/day/kg'
                                ax1_1 = np.log10(gen_alg1[i][gen_alg1[i] > 0])
                                p1 = make_plot(chart_title, ax1_1, label)
                                column.children.append(p1)
                            if j == "airborne_release":
                                label = '1/min/day/kg'
                                ax2_1 = np.log10(gen_alg2[i][gen_alg2[i] > 0])
                                p2 = make_plot(chart_title, ax2_1, label)
                                column.children.append(p2)
                            if j == "conti_release" :
                                label = '1/kg'
                                ax3_1 = np.log10(gen_alg3[i][gen_alg3[i] > 0])
                                p3 = make_plot(chart_title, ax3_1, label)
                                column.children.append(p3)
                            if j == "surface_volatilization" :
                                label = 'mg/day/kg'
                                ax4_1 = np.log10(gen_alg4[i][gen_alg4[i] > 0])
                                p4 = make_plot(chart_title, ax4_1, label)
                                column.children.append(p4)
                            if j == "liquid_contact":
                                label = 'mg/day/kg'
                                ax5_1 = np.log10(gen_alg5[i][gen_alg5[i] > 0])
                                p5 = make_plot(chart_title, ax5_1, label)
                                column.children.append(p5)
                            if j == "spraying_contact":
                                label = 'min/day'
                                ax6_1 = np.log10(gen_alg6[i][gen_alg6[i] > 0])
                                p6 = make_plot(chart_title, ax6_1, label)
                                column.children.append(p6)
                return column
            def Exposure_intensity():
                column = create_Exposure_intensity()
                return pn.Column(column)

            def _markdown(text):
                return bokeh.models.widgets.markups.Div(
                    text=markdown.markdown(text), sizing_mode="stretch_width"
                )

            product_content = pd.read_csv('product_chem_final.csv', encoding = 'CP949')

            def create_Distribution_exposure_product_table() :
                text = """  
                """
                data = dict(
                    col = [5,50,75,90,95,99],
                    dates=p2_table_data,
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="분위",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                data_table_all = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=390, height=390, sizing_mode="fixed"
                )
                data = dict(
                    col = [5,50,75,90,95,99],
                    dates=p3_table_data,
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="분위",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                data_table_m = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=200, height=390, sizing_mode="fixed"
                )
                data = dict(
                    col = [5,50,75,90,95,99],
                    dates=p4_table_data,
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="분위",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                data_table_w = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=200, height=390, sizing_mode="fixed"
                )

                grid = bokeh.layouts.grid(
                    children=[
                        _markdown(text),
                        [data_table_all],
                        [data_table_m],
                        [data_table_w],
                    ],
                )
                return grid


            def create_Distribution_exposure_product() :
                text = """
                """
                data = dict(
                    col = [5,50,75,90,95,99],
                    dates=p2_table_data,
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="분위",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                data_table_all = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=390, height=390, sizing_mode="fixed"
                )
                data = dict(
                    col = [5,50,75,90,95,99],
                    dates=p3_table_data,
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="분위",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                data_table_m = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=390, height=390, sizing_mode="fixed"
                )
                data = dict(
                    col = [5,50,75,90,95,99],
                    dates=p4_table_data,
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="분위",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                data_table_w = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=390, height=390, sizing_mode="fixed"
                )
                data = dict(
                    col = [5,50,75,90,95,99],
                    dates=p6_table_data,
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="분위",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                inh_data_table_all = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=390, height=390, sizing_mode="fixed"
                )
                
                grid = bokeh.layouts.grid(
                    children=[
                        _markdown(text),
                        [p13,p19],
                        #[p19],
                        [_markdown(text)],
                        [p14, data_table_all],
                        [_markdown(text)],
                        [p18, inh_data_table_all],
                        [_markdown(text)],
                        [p15, data_table_m],
                        [_markdown(text)],
                        [p16, data_table_w],
                    ],
                )
                return grid

            def Distribution_exposure_product():
                grid = create_Distribution_exposure_product()
                return pn.Column(grid)


            def create_Cumulative_exposure_distribution_table(table_data) :
                text = """
                """
                data = dict(
                    col = [5,50,75,90,95,99],
                    dates=table_data,
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="분위",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                data_table_all = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=390, height=390, sizing_mode="fixed"
                )
                return data_table_all

            def create_Cumulative_exposure_distribution() :
                text = """
                """
                column = bokeh.layouts.column(
                    _markdown(text),
                    sizing_mode="stretch_width"
                )
                table_column = bokeh.layouts.column(
                    _markdown(text),
                    sizing_mode="stretch_width"
                )
                tot_prod = np.sum(alg_sum, axis=0)
                tot_prod_df = pd.DataFrame(tot_prod, columns=["total_exposure"])
                sort_tot_prod_df = tot_prod_df.sort_values(by=['total_exposure'], axis=0, ascending=False)
                if len(selected_product_list) < 5:
                    sort_tot_prod_df_order = sort_tot_prod_df[:len(selected_product_list)]
                    for i in range(len(selected_product_list)):
                        table_data = [format(np.percentile(
                            alg_sum[:, sort_tot_prod_df_order.index[i]][alg_sum[:, sort_tot_prod_df_order.index[i]] > 0], 5), '.2E'),
                                    format(np.percentile(alg_sum[:, sort_tot_prod_df_order.index[i]][
                                                            alg_sum[:, sort_tot_prod_df_order.index[i]] > 0], 50), '.2E'),
                                    format(np.percentile(alg_sum[:, sort_tot_prod_df_order.index[i]][
                                                            alg_sum[:, sort_tot_prod_df_order.index[i]] > 0], 75), '.2E'), format(
                                np.percentile(
                                    alg_sum[:, sort_tot_prod_df_order.index[i]][alg_sum[:, sort_tot_prod_df_order.index[i]] > 0],
                                    90), '.2E'),
                                    format(np.percentile(alg_sum[:, sort_tot_prod_df_order.index[i]][
                                                            alg_sum[:, sort_tot_prod_df_order.index[i]] > 0], 95), '.2E'), format(
                                np.percentile(
                                    alg_sum[:, sort_tot_prod_df_order.index[i]][alg_sum[:, sort_tot_prod_df_order.index[i]] > 0],
                                    99), '.2E')]
                        table = create_Cumulative_exposure_distribution_table(table_data)

                        start_date = np.log10(np.percentile(alg_sum[:, sort_tot_prod_df_order.index[i]][alg_sum[:, sort_tot_prod_df_order.index[i]] > 0], 95))
                        end_date = np.log10(1.0)

                        ax1 = np.log10(alg_sum[:, sort_tot_prod_df_order.index[i]][alg_sum[:, sort_tot_prod_df_order.index[i]] > 0])
                        ax1 = np.sort(ax1)
                        plt = bokeh.plotting.figure(sizing_mode="fixed", width=800, height=390, x_range = (min(ax1[0], end_date) - (max(ax1[-1], end_date) - min(ax1[0], end_date)) * 0.2, max(ax1[-1], end_date) + (max(ax1[-1], end_date) - min(ax1[0], end_date)) * 0.4))
                        plt.xaxis.axis_label = '노출량 (mg/kg/day)'
                        plt.yaxis.axis_label = '빈도 (상대빈도)'
                        plt_title = product_content[product_content['code'] == selected_product_list[sort_tot_prod_df_order.index[i]]][
                            'category'].values[0]
                        plt_title = plt_title + product_content[product_content['code'] == selected_product_list[sort_tot_prod_df_order.index[i]]][
                            'use'].values[0]
                        plt_title = plt_title + product_content[product_content['code'] == selected_product_list[sort_tot_prod_df_order.index[i]]][
                            'type'].values[0]
                        plt.title.text = plt_title

                        hist, edges = np.histogram(ax1, density=True, bins=50)

                        daylight_savings_start = bokeh.models.Span(location=start_date,
                                                                dimension='height', line_color='red',
                                                                line_dash='dashed', line_width=1)
                        daylight_savings_start_label = bokeh.models.Label(text_color=daylight_savings_start.line_color, text='95th',
                                                                        x=daylight_savings_start.location + 0.01, y=max(hist)*.15)
                        plt.renderers.extend([daylight_savings_start, daylight_savings_start_label])

                        plt.quad(top=hist, bottom=0,color='#4673eb', alpha=0.3, left=edges[:-1], right=edges[1:])
                        plt.xaxis[0].formatter = FuncTickFormatter(code="""
                                    var str = tick.toString(); //get exponent
                                    var newStr = "";
                                    for (var i=0; i<10;i++)
                                    {
                                        var code = str.charCodeAt(i);
                                        switch(code) {
                                        case 45: // "-"
                                            newStr += "⁻";
                                            break;
                                        case 48: // "0"
                                            newStr +="⁰";
                                            break;
                                        case 49: // "1"
                                            newStr +="¹";
                                            break;
                                        case 50: // "2"
                                            newStr +="²";
                                            break;
                                        case 51: // "3"
                                            newStr +="³"
                                            break;
                                        case 52: // "4"
                                            newStr +="⁴"
                                            break;
                                        case 53: // "5"
                                            newStr +="⁵"
                                            break;                
                                        case 54: // "6"
                                            newStr +="⁶"
                                            break;
                                        case 55: // "7"
                                            newStr +="⁷"
                                            break;
                                        case 56: // "8"
                                            newStr +="⁸"
                                            break;
                                        case 57: // "9"
                                            newStr +="⁹"
                                            break;                         
                                        }
                                    }
                                    return 10+newStr;
                                    """)
                        plt.axis.major_label_text_font = "sans"
                        column.children.append(bokeh.layouts.grid(children=[[plt, table],[_markdown(text)]],))
                        table_column.children.append(table)
                else:
                    sort_tot_prod_df_5th = sort_tot_prod_df[:5]
                    for i in range(5):
                        table_data = [format(np.percentile(alg_sum[:,sort_tot_prod_df_5th.index[i]][alg_sum[:,sort_tot_prod_df_5th.index[i]] > 0], 5),'.2E'),
                                    format(np.percentile(alg_sum[:,sort_tot_prod_df_5th.index[i]][alg_sum[:,sort_tot_prod_df_5th.index[i]] > 0], 50),'.2E'),
                                    format(np.percentile(alg_sum[:,sort_tot_prod_df_5th.index[i]][alg_sum[:,sort_tot_prod_df_5th.index[i]] > 0], 75),'.2E'),
                                    format(np.percentile(alg_sum[:,sort_tot_prod_df_5th.index[i]][alg_sum[:,sort_tot_prod_df_5th.index[i]] > 0], 90),'.2E'),
                                    format(np.percentile(alg_sum[:,sort_tot_prod_df_5th.index[i]][alg_sum[:,sort_tot_prod_df_5th.index[i]] > 0], 95),'.2E'),
                                    format(np.percentile(alg_sum[:,sort_tot_prod_df_5th.index[i]][alg_sum[:,sort_tot_prod_df_5th.index[i]] > 0], 99),'.2E')]
                        table = create_Cumulative_exposure_distribution_table(table_data)

                        start_date = np.log10(np.percentile(alg_sum[:,sort_tot_prod_df_5th.index[i]][alg_sum[:,sort_tot_prod_df_5th.index[i]] > 0], 95))
                        end_date = np.log10(1.0)

                        ax1 = np.log10(alg_sum[:,sort_tot_prod_df_5th.index[i]][alg_sum[:,sort_tot_prod_df_5th.index[i]] > 0])
                        ax1 = np.sort(ax1)
                        plt = bokeh.plotting.figure(sizing_mode="fixed", width=800, height=390, x_range = (min(ax1[0], end_date) - (max(ax1[-1], end_date) - min(ax1[0], end_date)) * 0.2, max(ax1[-1], end_date) + (max(ax1[-1], end_date) - min(ax1[0], end_date)) * 0.4))
                        plt.xaxis.axis_label = '노출량 (mg/kg/day)'
                        plt.yaxis.axis_label = '빈도 (상대빈도)'
                        plt_title = product_content[product_content['code'] == selected_product_list[sort_tot_prod_df_5th.index[i]]][
                            'category'].values[0]
                        plt_title = plt_title + product_content[product_content['code'] == selected_product_list[sort_tot_prod_df_5th.index[i]]][
                            'use'].values[0]
                        plt_title = plt_title + product_content[product_content['code'] == selected_product_list[sort_tot_prod_df_5th.index[i]]][
                            'type'].values[0]
                        plt.title.text = plt_title

                        hist, edges = np.histogram(ax1, density=True, bins=50)

                        daylight_savings_start = bokeh.models.Span(location=start_date,
                                                                dimension='height', line_color='red',
                                                                line_dash='dashed', line_width=1)
                        daylight_savings_start_label = bokeh.models.Label(text_color=daylight_savings_start.line_color, text='95th',
                                                                        x=daylight_savings_start.location + 0.01, y=max(hist)*.15)
                        plt.renderers.extend([daylight_savings_start, daylight_savings_start_label])


                        plt.quad(top=hist, bottom=0, color='#4673eb', alpha=0.3, left=edges[:-1], right=edges[1:])

                        plt.xaxis[0].formatter = FuncTickFormatter(code="""
                        var str = tick.toString(); //get exponent
                        var newStr = "";
                        for (var i=0; i<10;i++)
                        {
                            var code = str.charCodeAt(i);
                            switch(code) {
                            case 45: // "-"
                                newStr += "⁻";
                                break;
                            case 48: // "0"
                                newStr +="⁰";
                                break;
                            case 49: // "1"
                                newStr +="¹";
                                break;
                            case 50: // "2"
                                newStr +="²";
                                break;
                            case 51: // "3"
                                newStr +="³"
                                break;
                            case 52: // "4"
                                newStr +="⁴"
                                break;
                            case 53: // "5"
                                newStr +="⁵"
                                break;                
                            case 54: // "6"
                                newStr +="⁶"
                                break;
                            case 55: // "7"
                                newStr +="⁷"
                                break;
                            case 56: // "8"
                                newStr +="⁸"
                                break;
                            case 57: // "9"
                                newStr +="⁹"
                                break;                         
                            }
                        }
                        return 10+newStr;
                        """)
                        plt.axis.major_label_text_font = "sans"
                        column.children.append(bokeh.layouts.grid(children=[[plt, table],[_markdown(text)] ], ))
                        table_column.children.append(table)
                return column, table_column

            def Cumulative_exposure_distribution():

                column, table_column = create_Cumulative_exposure_distribution()
                return pn.Column(column)

            # def create_Contribution_product() :
            #     text = """
            #     """
            #     column = bokeh.layouts.Column(
            #         children=[_markdown(text),p17])
                return column
            def Contribution_product():
                labels = list(data.country)
                portion_list = list(data.value)
                fig = go.Figure(data=[go.Pie(labels=labels, values=portion_list, hole=.5)])
                fig.update_layout(width=720, height=500,title="제품별 전신 노출 기여도")
                return pn.Column(fig)

            def pie_inh():
                labels = list(p20.index)
                portion_list = list(p20.value)
                fig = go.Figure(data=[go.Pie(labels=labels, values=portion_list, hole=.5)])
                fig.update_layout(width=720, height=500,title="제품별 흡입 노출 기여도")
                return pn.Column(fig)
                
            def summary():
                selected_product_content = product_content[product_content["CAS"] == input_chemical]
                substance_name = selected_product_content.iloc[0, 1]

                text = '## </br></br> * 물질명 : ' + str(substance_name) + '</br></br>' + '* CAS No. : ' + input_chemical + '</br></br></br> * 물질정보'
                text1 = '## * 함유 제품 정보 (초록누리)'
                # text2 = '</br></br> * 제품별 노출량'
                # text3 = '누적 노출분포'
                # text4 = '제품별 기여도'

                data = dict(
                    col = ['분자량 [g/mole]','증기압 [Pa]','경피 흡수율 [-]','흡입 흡수율 [-]'],
                    dates=[M, P_vap, der_abs, inh_abs]
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="col", title="물질정보(단위)",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="dates", title="노출량 (mg/kg/day)",
                    ),
                ]
                Substance_information_table = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=400, height=390, sizing_mode="fixed"
                )

                data = dict(
                    product_name = selected_product_content["product_name"],
                    category = selected_product_content["category"],
                    type = selected_product_content["type"],
                    conc_min = selected_product_content["conc_min"],
                    conc_max = selected_product_content["conc_max"],
                )
                source = bokeh.models.ColumnDataSource(data)

                columns = [
                    bokeh.models.widgets.TableColumn(
                        field="product_name", title="product_name",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="category", title="category",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="type", title="type",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="conc_min", title="함유량(최소) (%)",
                    ),
                    bokeh.models.widgets.TableColumn(
                        field="conc_max", title="함유량(최대) (%)",
                    ),
                ]

                product_information_table = bokeh.models.widgets.DataTable(
                    source=source, columns=columns, width=700, height=390, sizing_mode="fixed"
                )

                text_column1 = _markdown(text)
                text_column2 = _markdown(text1)
                # text_column3 = _markdown(text2)
                # text_column4 = _markdown(text3)
                # text_column5 = _markdown(text4)
                #column1 = create_Exposure_intensity()
                # column2 = create_Distribution_exposure_product_table()
                # column3, table_column = create_Cumulative_exposure_distribution()
                # column4 = create_Contribution_product()

                layout = bokeh.layouts.layout([
                    [text_column1],
                    [Substance_information_table],
                    [text_column2],
                    [product_information_table],
                    # [text_column3],
                    # [column2],
                    # [text_column4],
                    # [table_column],
                    # [text_column5],
                    # [column4],
                ])

                return pn.Column(layout)
            mark13=pn.pane.Markdown("<brt><br>")
            flow_4=pn.Column(pn.pane.JPG('소지바제품 누적 통합 노출량 산정 절차 그림.jpg',height=470,width=800),pn.pane.JPG('노출강도 설명 그림.jpg',height=470,width=800))
            @pn.depends(x=radio_group5.param.value)
            def main_s(x):
                if x =='입력정보확인':
                    tab=pn.Column(flow_4,summary(),mark13,Exposure_intensity())
                elif x=='누적노출분포':
                    tab=Distribution_exposure_product()
                elif x=='제품별노출분포':
                    tab=Cumulative_exposure_distribution()
                elif x=='제품별기여도':
                    tab=pn.Column(Contribution_product(),pie_inh())
                return pn.Column(radio_group5,tab)
            tabs=pn.Column(main_s)
            tabs.background="#ffffff"
        elif radio_group.value=='통합노출':

            indirect_exposure = pd.read_csv("indirect.csv", encoding='CP949')
            direct_exposure = pd.read_csv("exposure.csv", encoding='CP949')


            if (indirect_exposure['chemi']==chemi_input.value).any() & (direct_exposure['chemi']==chemi_input.value).any():


                choose_num = 1000
                repeat_num = 100


                indirect_exposure_sampling = np.random.choice(indirect_exposure['exp'], choose_num)
                direct_exposure_sampling = np.random.choice(direct_exposure['exposure'], choose_num)

                result = indirect_exposure_sampling + direct_exposure_sampling


                result_df = pd.DataFrame(index=range(0,choose_num), columns=range(0,repeat_num))



                for i in range(repeat_num):
                    indirect_exposure_sampling = np.random.choice(indirect_exposure['exp'], choose_num)
                    direct_exposure_sampling = np.random.choice(direct_exposure['exposure'], choose_num)

                    result = indirect_exposure_sampling + direct_exposure_sampling
                    result_sorted = np.sort(result)
                    result_df.iloc[:,i] = result_sorted
                    


                a = np.mean(result_df, axis=1)
                a_min = np.min(result_df, axis=1)
                a_max = np.max(result_df, axis=1)

                a_y = 1. * np.arange(len(a)) / (len(a) - 1)



                result_df = pd.DataFrame({'exp':a, 'cdf':a_y})
                result_min_df = pd.DataFrame({'exp':a_min, 'cdf':a_y})
                result_max_df = pd.DataFrame({'exp':a_max, 'cdf':a_y})


                fig5 = go.Figure([
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

                fig5.update_layout(
                    xaxis_title='노출량 (mg/kg/day)',
                    yaxis_title='CDF',
                    title='통합 노출량 (mg/kg/day)',
                    hovermode="x",
                    width=850,
                    height=550,
                )
                fig5.update_layout(xaxis_type="log")
                title=pn.pane.Markdown("## 통합 노출량 그래프 "+"("+chemi_input.value+")"+"<br> ", style={'font-family': 'NanumBarunGothic','font-size':'20px'},sizing_mode='stretch_width')
                tabs=pn.Column(title,fig5)
            else:
                caution_marks=pn.pane.Markdown("## 간접 노출과 직접 노출 산정에 사용된 물질이 같은 물질인지 확인해주세요 ", style={'font-family': 'NanumBarunGothic','font-size':'20px'})
                tabs=pn.Column(caution_marks)
    return tabs
mark7=pn.pane.Markdown("## 화학물질 선택")
## SERVE
template = pn.template.MaterialTemplate(
    site="EHR&C", title="활동공간 및 소비자제품 인체 노출량 연산 프로그램" ,
    # sidebar=[side_area],
    sidebar=[radio_group_shp,selector,search_chemi],
    main=[calculate_A_batch]
    # main=[area]

)

template.sidebar_width=800
template.servable()