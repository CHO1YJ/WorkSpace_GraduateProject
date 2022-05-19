import numpy as np

# 3차선 삼거리 도로라고 가정!
# 실시간 카운트에 따른 거의 무한루프식의 제어를 가정!

# 신호등 패턴 조절 함수가 전달받는 값
# 이거 2차선이랑 3차선 합해서 카운트 못하나????????????? 어차피 직진이니까?
count_car_1 = 4 # 1차선 차량 카운트; 좌회전 차량
count_car_2 = 4 # 2차선 차량 카운트; 직진 차량
count_car_3 = 5 # 3차선 차량 카운트; 직진 차량
count_bus_1 = 1 # 1차선 버스 카운트
count_bus_2 = 0 # 2차선 버스 카운트
count_bus_3 = 0 # 3차선 버스 카운트
count_emergency_1 = 0 # 1차선 구급차 카운트
count_emergency_2 = 0 # 2차선 구급차 카운트
count_emergency_3 = 0 # 3차선 구급차 카운트
count_people = 0 # 보행자 카운트

# 신호등 패턴 조절 함수의 변수 설정 
# 차량용 보행자용 총 시간은 각각 60초로 기준 설정
time_car_r = 28 # 차량용 신호등 적색등 점등 시간
time_car_y = 4 # 차량용 신호등 황색등 점등 시간
time_car_g_left = 14 # 차량용 신호등 좌회전등 점등 시간; 직진 신호랑 겹침
time_car_g_stright = 28 # 차량용 신호등 녹색등 점등 시간
time_peo_r = 30 # 보행자용 신호등 적색등 점등 시간
time_peo_g = 30 # 보행자용 신호등 녹색등 점등 시간

weight_bus = 2 # 크기로 볼 때, 일반 차량의 2배로 생각
# 시간 변화량 정의
t_var_car = 1
t_var_pple = 1

def Control_Traffic_Lights_by_Car(cnt_car1, cnt_car2, cnt_car3, \
                                  cnt_bus1, cnt_bus2, cnt_bus3,
                                  cnt_emgncy1, cnt_emgncy2, cnt_emgncy3, \
                                      cnt_pple):
    # 직진 및 좌회전 시의 차량 및 구급차, 소방차 대수 계산
    cnt_left = cnt_car1 + cnt_bus1 * weight_bus
    cnt_straight = cnt_car2 + cnt_car3 + (cnt_bus2 + cnt_bus3) * weight_bus
    cnt_emgncy_left = cnt_emgncy1
    cnt_emgncy_straight = cnt_emgncy2 + cnt_emgncy3
    
    flag_emergency = False # 구급차, 소방차 인식되면 True / 평시 False
    flag_silver = False # 노약자 및 휠체어가 인식되면 True / 평시 False
    
    # 긴급 상황 발생
    if cnt_emgncy_straight > 0 or cnt_emgncy_left > 0:
        flag_emergency = True
        
    if flag_emergency == False: # 평시
        if cnt_straight >= cnt_left:
            t_car_g_strit = time_car_g_stright + t_var_car
            t_car_g_lft = time_car_g_left - t_var_car
        elif cnt_straight < cnt_left:
            t_car_g_strit = time_car_g_stright - t_var_car
            t_car_g_lft = time_car_g_left - t_var_car
        else: # 긴급 상황
            if cnt_emgncy_straight > 0:
                t_car_g_strit = 60
                time_car_g_left = 60
            elif cnt_emgncy_left > 0:
                t_car_g_strit = 60
                time_car_g_left = 60
                
            flag_emergency = False

    return t_car_g_strit, t_car_g_lft # 차량 신호등 직진 좌회전 시간 제어

# 함수 호출
time_car_g_stright, time_car_g_left = \
    Control_Traffic_Lights_by_Car(count_car_1, count_car_2, count_car_3, \
                              count_bus_1, count_bus_2, count_bus_3, \
                                  count_emergency_1, count_emergency_2, \
                                      count_emergency_3, count_people)
                             