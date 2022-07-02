import numpy as np
import json


def init_data():
    # 입력 파일에 대한 코딩이 필요
    with open('json_data/Traffic_lights_data.json', 'r', encoding="UTF-8") as f:
        # 1. json 파일을 읽어오는 함수 load를 사용하는 방식
        json_data = json.load(f)

    # 4차선 삼거리 도로라고 가정!

    # 서버를 통해 전달받은 차량용 신호등에서 차량의 카운트 값
    count_car_1 = json_data["Traffic_Light_Cars"][0]["Cars_1"]  # 1차선 차량 카운트; 좌회전 차량
    count_car_2 = json_data["Traffic_Light_Cars"][1]["Cars_2"]  # 2차선 차량 카운트; 직진 차량
    count_bus_1 = json_data["Traffic_Light_Cars"][0]["Bus_1"] + \
                  json_data["Traffic_Light_Cars"][0]["Truck_1"]  # 1차선 버스 및 트럭 카운트
    count_bus_2 = json_data["Traffic_Light_Cars"][1]["Bus_2"] + \
                  json_data["Traffic_Light_Cars"][1]["Truck_2"]  # 2차선 버스 및 트럭 카운트
    count_emergency_1 = json_data["Traffic_Light_Cars"][0]["Firetruck_1"] + \
                        json_data["Traffic_Light_Cars"][0]["Ambulance_1"]  # 1차선 구급차 및 소방차 카운트
    count_emergency_2 = json_data["Traffic_Light_Cars"][1]["Firetruck_2"] + \
                        json_data["Traffic_Light_Cars"][1]["Ambulance_2"]  # 2차선 구급차 및 소방차 카운트
    weight_bus = 2  # 크기로 볼 때, 일반 차량의 2배로 생각
    data_traffic_lights_car = {
        'count_car_1': count_car_1,
        'count_car_2': count_car_2,
        'count_bus_1': weight_bus * count_bus_1,
        'count_bus_2': weight_bus * count_bus_2,
        'count_emergency_1': count_emergency_1,
        'count_emergency_2': count_emergency_2,
    }

    # 서버를 통해 전달받은 보행자용 신호등에서 사람의 카운트 값
    count_people = json_data["Traffic_Light_People"][0]["People"]  # 보행자 카운트
    count_silver = json_data["Traffic_Light_People"][0]["Silver"]  # 노약자 카운트
    count_wheel = json_data["Traffic_Light_People"][0]["Wheelchair"]  # 휠체어 카운트
    data_traffic_lights_people = {
        'count_people': count_people,
        'count_silver': count_silver,
        'count_wheel': count_wheel,
    }

    # 신호등 패턴 조절 함수의 변수 설정
    # 차량용 신호등의 기준 시간 합계는 110초로 설정
    standard_time_car_r = 30  # 차량용 신호등 적색등 점등 기준 시간
    t_car_r = 30  # 차량용 신호등 적색등 점등 변동 시간
    standard_time_car_y = 3  # 차량용 신호등 황색등 점등 기준 시간
    t_car_y = 3  # 차량용 신호등 황색등 점등 변동 시간
    standard_time_car_g_left = 21  # 차량용 신호등 좌회전등 점등 기준 시간
    t_car_g_l = 21  # 차량용 신호등 좌회전등 점등 변동 시간
    standard_time_car_g_straight = 57  # 차량용 신호등 녹색등 점등 기준 시간
    t_car_g_s = 57  # 차량용 신호등 좌회전등 점등 변동 시간
    # 보행자용 신호등의 기준 시간 합계는 30초로 설정
    standard_time_peo_g = 30  # 보행자용 신호등 녹색등 점등 기준 시간
    t_pple_g = 30  # 보행자용 신호등 녹색등 점등 변동 시간
    data_traffic_lights_time = {
        'standard_time_car_r': standard_time_car_r, 't_car_r': t_car_r,
        'standard_time_car_y': standard_time_car_y, 't_car_y': t_car_y,
        'standard_time_car_g_left': standard_time_car_g_left, 't_car_g_l': t_car_g_l,
        'standard_time_car_g_straight': standard_time_car_g_straight, 't_car_g_s': t_car_g_s,
        'standard_time_peo_g': standard_time_peo_g, 't_pple_g': t_pple_g
    }

    # 시간 변화량 정의
    t_var_car = 1
    t_var_pple = 1
    data_traffic_lights_hyper_parameter = {
        't_var_car': t_var_car,
        't_var_pple': t_var_pple
    }

    flag_emergency = False  # 구급차, 소방차 인식되면 True / 평시 False
    flag_silver = False  # 노약자 및 휠체어가 인식되면 True / 평시 False
    flag_lights_on_car = json_data["flag_lights_on"][0]["lights_car"]
    if flag_lights_on_car == "True":
        flag_lights_on_car = True
    elif flag_lights_on_car == " False":
        flag_lights_on_car = False
    flag_lights_on_ppl = json_data["flag_lights_on"][0]["lights_people"]
    if flag_lights_on_ppl == "True":
        flag_lights_on_ppl = True
    elif flag_lights_on_ppl == " False":
        flag_lights_on_ppl = False
    data_specific_flag = {
        'flag_emergency': flag_emergency,
        'flag_silver': flag_silver,
        'flag_lights_on_car' : flag_lights_on_car,
        'flag_lights_on_ppl' : flag_lights_on_ppl
    }

    return data_traffic_lights_car, data_traffic_lights_people, data_traffic_lights_time, \
           data_traffic_lights_hyper_parameter, data_specific_flag


# 최대 및 최소 시간제한 함수
def limit_time(data_lights_time_lt):
    standard_time = np.array([data_lights_time_lt['standard_time_car_r'],
                              data_lights_time_lt['standard_time_car_y'],
                              data_lights_time_lt['standard_time_car_g_left'],
                              data_lights_time_lt['standard_time_car_g_straight'],
                              data_lights_time_lt['standard_time_peo_g']])
    var_time = np.array([data_lights_time_lt['t_car_r'],
                              data_lights_time_lt['t_car_y'],
                              data_lights_time_lt['t_car_g_l'],
                              data_lights_time_lt['t_car_g_s'],
                              data_lights_time_lt['t_pple_g']])
    max_time = standard_time + standard_time / 2  # 시간의 최대값
    min_time = standard_time - standard_time / 2  # 시간의 최소값
    for n in range(len(var_time)):
        if var_time[n] < min_time[n]:  # 변동시간이 최대값을 넘어선 경우
            var_time[n] = min_time[n]
        elif var_time[n] > max_time[n]:  # 변동시간이 최소값을 넘어선 경우
            var_time[n] = max_time[n]
    return var_time  # 변동 시간 반환


# 긴급 차량 및 교통약자 확인 함수
def flag_func(data_lights_car_ff, data_lights_people_ff, data_spec_flag_ff):
    cnt_emergency_1 = data_lights_car_ff['count_emergency_1']
    cnt_emergency_2 = data_lights_car_ff['count_emergency_2']
    cnt_silver = data_lights_people_ff['count_silver']
    cnt_wheel = data_lights_people_ff['count_wheel']
    flag_car = data_spec_flag_ff['flag_emergency']
    flag_people = data_spec_flag_ff['flag_silver']

    if cnt_emergency_1 > 0 or cnt_emergency_2 > 0:  # 긴급 차량 확인
        flag_car = True
    else:
        flag_car = False

    if cnt_silver > 0 or cnt_wheel > 0:  # 교통 약자 확인
        flag_people = True
    else:
        flag_people = False

    data_spec_flag_ff['flag_emergency'] = flag_car
    data_spec_flag_ff['flag_silver'] = flag_people
    return data_spec_flag_ff  # 차량용 및 보해앚용 신호등의 긴급 상황 flag 반환


# 신호등 제어 알고리즘 함수
def run_control_traffic_lights(data_lights_car_run,
                               data_lights_people_run,
                               data_lights_time_run,
                               data_lights_hyper_parameter_run,
                               data_specific_flag_run
                               ):
    # 직진 및 좌회전 시의 차량 및 구급차, 소방차 대수 계산
    cnt_left = sum(data_lights_car_run.values())  # 1차선; 좌회전도 직진도 가능한 차선의 차량 수
    cnt_straight = sum(data_lights_car_run.values())  # 2차선; 직진만 가능한 차선의 차량 수
    cnt_total_cars = sum(data_lights_car_run.values())

    # 횡단보도에서 인식된 사람들 및 노약자와 휠체어 수 계산
    cnt_total_peo = sum(data_lights_people_run.values())  # 전체 사람 수

    t_car_r_run = data_lights_time_run['t_car_r']
    t_car_y_run = data_lights_time_run['t_car_y']
    t_car_g_l_run = data_lights_time_run['t_car_g_l']
    t_car_g_s_run = data_lights_time_run['t_car_g_s']
    t_pple_g_run = data_lights_time_run['t_pple_g']

    t_var_car_run = data_lights_hyper_parameter_run['t_var_car']

    # 특수 상황 발생 여부 확인 - 구급차, 소방차, 교통약자(노약자, 휠체어) 인식
    data_specific_flag_run = \
        flag_func(data_lights_car_run, data_lights_people_run, data_specific_flag_run)
    flag_car_run = data_specific_flag_run['flag_emergency']
    flag_people_run = data_specific_flag_run['flag_silver']
    flag_lights_on_car_run = data_specific_flag_run['flag_lights_on_car']
    flag_lights_on_ppl_run = data_specific_flag_run['flag_lights_on_ppl']

    # 차량 및 보행자용 신호등 제어 알고리즘
    # 평시
    if flag_car_run == False and flag_people_run == False:
        # 변동 적용 시간 한계 설정
        data_lights_limit_time = limit_time(data_lights_time_run)
        t_car_r_run = data_lights_limit_time[0] # 차량용 - 적색
        t_car_y_run = data_lights_limit_time[1] # 차량용 - 황색
        t_car_g_l_run = data_lights_limit_time[2] # 차량용 - 좌회전
        t_car_g_s_run = data_lights_limit_time[3] # 차량용 - 직진
        t_pple_g_run = data_lights_limit_time[4] # 보행자용 - 녹색

        # 차도가 인도보다 복잡한 경우 - 차량 수가 사람 수보다 많을 경우
        if cnt_total_cars > cnt_total_peo:
            if cnt_straight >= cnt_left:  # 직진 차량이 좌회전 차량보다 많을 경우
                t_car_g_s_run = t_car_g_s_run + t_var_car_run  # 직진 신호 시간 증가
            elif cnt_straight <= cnt_left:  # 좌회전 차량이 직진 차량보다 많을 경우
                t_car_g_l_run = t_car_g_l_run + t_var_car_run  # 좌회전 신호 시간 증가
        # 인도가 차도보다 복잡한 경우 - 사람 수가 차량 수보다 많을 경우
        elif cnt_total_cars < cnt_total_peo:
            if cnt_total_peo > 5:  # 이 제어를 해야하나 안 해야하나? 테스트를 통해 확인 필요
                t_car_g_s_run = t_car_g_s_run - t_var_car_run  # 직진 신호 시간 감소
                t_car_g_l_run = t_car_g_l_run - t_var_car_run  # 좌회전 신호 시간 감소

    # 두번째 if문 시간 조정 방식 수정 필요
    # 특수 상황 시
    # 노약자 및 휠체어 인식
    if flag_lights_on_ppl_run == True and flag_people_run == True:
        if t_pple_g_run < 5:  # 교통 약자가 지나갈 때까지 시간 고정
            t_pple_g_run = 5
    # 구급차, 소방차 인식
    if flag_lights_on_car_run == True and flag_car_run == True: 
        if t_car_g_s_run < 5 or t_car_g_l_run < 3:  # 구급차, 소방차가 지나갈 때까지 시간 고정
            t_car_g_l_run = 3
            t_car_g_s_run = 5

    result_lights_time_run = {
        't_car_r' : t_car_r_run, 
        't_car_y' : t_car_y_run, 
        't_car_g_l' : t_car_g_l_run, 
        't_car_g_s' : t_car_g_s_run, 
        't_pple_g' : t_pple_g_run
    }
    return result_lights_time_run


# 메인함수
def main():
    # 신호등 데이터 정제
    data_lights_car, data_lights_people, data_lights_time, \
    data_lights_hyper_parameter, data_specific_flag = init_data()

    # 제어 전 출력 테스트
    print("# 제어 전")
    print("차_적", data_lights_time['t_car_r'])
    print("차_황", data_lights_time['t_car_y'])
    print("차_초_좌", data_lights_time['t_car_g_l'])
    print("차_초_직", data_lights_time['t_car_g_s'])
    print("사_초", data_lights_time['t_pple_g'])
    print("")

    # 신호등 제어 동작 함수 - # 변동 시간 적용
    result_lights_time = run_control_traffic_lights(data_lights_car,  # 차량용 신호등 클래스 카운트 데이터
                                                    data_lights_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                    data_lights_time,  # 신호 패턴 시간 데이터
                                                    data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                    data_specific_flag)  # 특수 상황에 대한 신호 데이터

    # 제어 후 출력 테스트
    print("# 제어 후")
    print("차_적", result_lights_time['t_car_r'])
    print("차_황", result_lights_time['t_car_y'])
    print("차_초_좌", result_lights_time['t_car_g_l'])
    print("차_초_직", result_lights_time['t_car_g_s'])
    print("사_초", result_lights_time['t_pple_g'])

# 파일 실행 시점
if __name__ == "__main__":
    main()
