import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import folium
from folium.plugins import MarkerCluster


# ===================== Function Code ========================
# [ pie 그래프 출력을 위해 선언한 함수 ]
def draw_pie_plot(traffic) :
    user_chs_year = 0 # 사용자가 선택한 값을 저장할 변수 
    while True :    
        print('-------------------------')
        for i in range(0, len(traffic)) : # 데이터에 존재하는 연도 수 만큼 출력 
            print(f'{i + 1}. {traffic.index[i]}년도') # 데이터의 인덱스를 읽어서 사용자에게 표시 
        print('-------------------------')
        selected_graph = input('어떤 연도의 교통범규 단속 데이터를 출력하시겠습니까 : ')

        try: # try except를 활용하여 숫자외의 입력을 방지 
            judge = int(selected_graph) # 사용자의 입력 값을 정수변환
        except : # 사용자 입력이 정수가 아니면 실행 
            print('숫자만 입력하셔야 합니다!')
            continue
        
        if judge >= 1 and judge <= 5 : # 사용자가 1 ~ 5사이의 값을 입력했을 때
            user_chs_year = judge - 1 # 해당 연도의 번호를 별도 저장 
            break # 반복문 종료 
        else : 2
            print('1 ~ 5사이의 값만 입력하셔야 합니다!')

    label = traffic.columns # column 의 값을 라벨로 출력하기 위해 저장 
    data = traffic.loc[traffic.index[user_chs_year],:] # 사용자가 선택한 연도의 데이터를 별도 저장 

    def func(pct, allvals): # pie 그래프 내 데이터의 font를 지정하기 위해 사용하는 익명함수
        absolute = int(pct/100.*np.sum(allvals)) 
        # 데이터를 받아 numpy를 통해 pie 그래프에 표시될 교통사고 데이터를 출력
        return "{:.1f}%\n({:d} 명)".format(pct, absolute) # % 단위 출력 후, 줄바꾼 후 인원 수 출력

    plt.rc('font', family='Malgun Gothic')
    plt.figure(figsize=(9,6)) # 이미지 크기(가로 세로) 설정 
    plt.title(f'{traffic.index[user_chs_year]}년 울산 교통법규 단속', fontsize=23) # 제목
    plt.pie(data, 
            labels=label, # 라벨(리스트) 
            startangle=90, # 시작 각도
            shadow=True, # 그림자 생성 여부
            textprops=dict(color="w", fontsize=20), # pie 그래프 내의 글자 색과 크기
            explode=(0,0,0,0.15), # 그래프의 일부분을 띄움 
            autopct=lambda pct: func(pct, data) 
            # 람다식과 함수를 통해 pie 영역별 출력할 데이터의 형식 정의 
        )

    plt.tight_layout() # 현재 figure 상에 배치된 요소들의 공백을 적당하게 배치해주는 역할(필수는 아님)
    plt.legend(title="단속 종류", # 레전드의 타이틀
            loc='center left', # 레전드의 위치 
            bbox_to_anchor=(0.8,0.5), # x,y축 퍼센트 단위 위치(단 1 = 100%) 
            fontsize=15, # 글자 크기
        )
    plt.axis('equal') # pie 그래프가 균열없이 출력되도록 함
    plt.show()


# [ bar 그래프 출력시 실행 ]
def draw_bar_plot(traffic): 
    colors = ['orange', 'cadetblue', 'salmon', 'skyblue'] # 색깔 지정 

    plt.style.use('seaborn') # style 지정 
    plt.rc('font', family='Malgun Gothic') # 그래프의 글자 지정(시스템 내의 글자)

    bar = traffic.plot(kind='bar', # 그래프 종류 지정
            rot=0, # bar 그래프 이름 회전 여부
            width=0.8, # bar 그래프 넓이
            figsize=(13,8), # 창 사이즈(인치)
            color=colors # 그래프 색깔
        ) 

    plt.title('연도별 울산 교통법규 위반자', fontsize=23) # 제목과 글자 크기
    plt.legend(title='단속 종류', # 레전드의 라벨 이름 
            loc='center left', # 레전드의 위치 설정(왼쪽에서 중간)
            bbox_to_anchor=(0.95,0.5),  # 창 내에서 레전드 위치 (1 = 100$)
            fontsize=15, # 레전드의 글자 크기 지정 
        )
    plt.xlabel('연도', fontsize=17) # x축 라벨 설정
    plt.ylabel('적발자 수', fontsize=17) # y축 라벨 설정
    plt.xticks(fontsize=15) # x축 라벨의 글자 크기
    plt.yticks(fontsize=15) # y축 라벨의 글자 크기 

    for p in bar.patches: # bar 그래프 요소마다 값을 표시하기 위해 그래프 개수만큼 반복 
        left, bottom, width, height = p.get_bbox().bounds  # bar 그래프의 크기를 가져옴 
        bar.annotate('%d명'%height, xy=(left+width/2, bottom+height+300), 
                    ha='center', va='center', fontsize=13, color='#9900ff') 
        # bar 그래프에 표시될 데이터의 형식 및 위치를 지정(각 그래프별로 가로 세로 치수가 존재)
    plt.box(False) # 그래프의 배경색이 보이게 하지 않음 
    plt.show()


# [ Map으로 출력 시 실행 ]
def print_camera_map() :
    df = pd.read_csv('TrafficCamera.csv', encoding='cp949', delimiter=',')
    # Map에 표시하기 위해 위도 경도가 들어있는 CSV 파일을 가져옴 

    location_df = df.loc[df['장소'].str.contains('범서읍')].copy() 
    # 출력을 희망하는 구역의 데이터만 새로운 변수에 별도로 저장 
    del df # 필요한 데이터를 별도로 저장함으로 기존의 변수는 필요없으니 메모리를 위해 제거 
    
    location_df = location_df.groupby(['장소','제한속도','경도','위도'])['구분'].count()
    # 출력한 데이터만 group으로 묶어서 다시 변수에 저장 
    location_df = location_df.reset_index() # 새로 변수에 저장한 데이터에 새로운 index 할당 

    map = folium.Map( # map에 데이터의 위도와 경도를 읽어서 위치에 표시 
        location=[location_df['위도'].mean(), location_df['경도'].mean()],
        # 위도와 경도의 평균값을 구해, 인접한 위치에 있는 것을 하나로 묶음 
        zoom_start = 15, # 처음 화면의 zoom 위치 지정 
        tiles = 'cartodbpositron' # tile의 형식을 지정 
    ) 

    cluster = MarkerCluster().add_to(map) # 만약 요소가 많을 경우를 대비하여 클라스터 위에 지도를 그림

    for index in location_df.index : # 반복문을 통해 데이터 수만큼 반복하여 Marker로 표시 
        popup_str = f"{location_df['장소'][index]}<br> > 제한속도 {location_df['제한속도'][index]}"
        # popup에 표시할 문자열 지정(장소의 이름과 제한 속도를 popup에 표시)

        folium.Marker( # Marker의 위치 및 옵션 지정 
            [location_df['위도'][index], location_df['경도'][index]], # Marker의 위치 지정 
            popup = popup_str, # 위에서 작성한 popup 메세지를 가져옴 
            icon = folium.Icon(color='blue', icon='video-camera', prefix='fa') 
            # Marker의 색깔 아이콘(Font Awesome에서 camera이미지를 가져옴)
        ).add_to(cluster) # 클라스터(지도)에 추가 

    map.save('Beomseo.html') # 생성한 지도를 "범서"라는 이름으로 새로저장 
    print('성공적으로 파일을 생성하였습니다. 현재 폴더의 Beomseo.html를 열어주세요.')


# [ Python이 수행할 작업 선택 ]
def select_work() :
    while True : # 사용자가 제대로된 값을 입력할 때까지 무한 반복 
        print('1 : pie 그래프 => 연도별 울산 교통법규 위반 종류') # 안내 메세지
        print('2 : bar 그래프 => 14 ~ 18년도 울산 교통법규 단속 데이터') 
        print('3 : map 출력   => 울산 무인 교통단속 장비 설치 위치')
        selected_graph = input('어떤 작업을 수행하시겠습니까 : ') # 사용자로부터 입력받음 

        try: # try except를 활용하여 숫자외의 입력을 방지 
            judge = int(selected_graph) # 사용자의 입력 값을 정수변환
        except : 
            print('숫자만 입력하셔야 합니다!') # 사용자가 잘못된 값을 입력했을때 안내 메세지 
            continue # 밑의 코드는 생략하고 처음으로 되돌아감 
        
        if judge >= 1 and judge <= 3: 
            return judge # 사용자가 1 ~ 3사이의 값 입력시 해당 정수를 Main 코드로 반환 
        else :
            print('0과 1만 입력하셔야 합니다!')


# ===================== Main Code ========================
df = pd.read_csv('TrafficAccident.csv', encoding='cp949', delimiter=',')
# bar와 pie 그래프에 사용될 CSV 파일을 가져와서 df 변수에 저장 

traffic = df.loc[:,['연도별','음주','무면허','범법','보행자']].copy()
# CSV 파일에서 가져온 값에서 필요한 데이터만 모두 가져와서 bar 그래프에 사용될 변수 traffic_bar에 별도로 복사  

del df # 필요한 데이터는 복사했으므로 기존의 변수(데이터)는 메모리를 위해 제거 

traffic = traffic.set_index('연도별', drop = True) # index를 연도로 지정, 기존의 연도 행은 제거 

user_select = select_work() # 사용자가 Python이 수행할 작업 선택 

if user_select == 1: # 만약 사용자가 bar 그래프를 출력하고자 한다면 
    print('pie 그래프를 선택하셨습니다.')
    draw_pie_plot(traffic) # 필요한 데이터를 별도로 저장한 traffic 데이터를 매개변수로 준다
elif user_select == 2: # 만약 사용자가 pie 그래프를 출력하고자 한다면 
    print('bar 그래프를 선택하셨습니다.')
    draw_bar_plot(traffic) # 필요한 데이터를 별도로 저장한 traffic 데이터를 매개변수로 준다
elif user_select == 3: # 만약 사용자가 무인 단속장비의 위치를 알고자 한다면 
    print('지도 출력을 선택하셨습니다.')
    print_camera_map() # 지도에 위치가 표시된 html파일을 출력한다.
