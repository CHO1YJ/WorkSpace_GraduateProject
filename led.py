import _rpi_ws281x as ws
import numpy as np
import time  # 시간관련 모듈을 불러옴
import json

################################################################################

def init_data():
    # 입력 파일에 대한 코딩이 필요
    with open('json_data/Traffic_lights_data.json', 'r', encoding="UTF-8") as f:
        # 1. json 파일을 읽어오는 함수 load를 사용하는 방식
        json_data = json.load(f)

    # 4차선 삼거리 도로라고 가정!

    # 신호등 패턴 조절 함수의 변수 설정
    # 차량용 신호등의 기준 시간 합계는 100초로 설정
    standard_time_car_r = 30  # 차량용 신호등 적색등 점등 기준 시간
    t_car_r = 30  # 차량용 신호등 적색등 점등 변동 시간
    standard_time_car_y = 3  # 차량용 신호등 황색등 점등 기준 시간
    t_car_y = 3  # 차량용 신호등 황색등 점등 변동 시간
    standard_time_car_g_left = 20  # 차량용 신호등 좌회전등 점등 기준 시간
    t_car_g_l = 20  # 차량용 신호등 좌회전등 점등 변동 시간
    standard_time_car_g_straight = 50  # 차량용 신호등 녹색등 점등 기준 시간
    t_car_g_s = 50  # 차량용 신호등 좌회전등 점등 변동 시간
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

    return data_traffic_lights_time, data_traffic_lights_hyper_parameter, data_specific_flag

def update_data(data_lights_flag_ud):
    # 입력 파일에 대한 코딩이 필요
    with open('json_data/Traffic_lights_data.json', 'r', encoding="UTF-8") as f:
        # 1. json 파일을 읽어오는 함수 load를 사용하는 방식
        json_data = json.load(f)
    weighted_value = 2
    update_lights_car = {
        'cnt_car_1' : json_data["Traffic_Light_Cars"][0]["Cars_1"],
        'cnt_car_2' : json_data["Traffic_Light_Cars"][1]["Cars_2"],
        'cnt_bus_1' : weighted_value * (json_data["Traffic_Light_Cars"][0]["Bus_1"] + \
                                        json_data["Traffic_Light_Cars"][0]["Truck_1"]),
        'cnt_bus_2' : weighted_value * (json_data["Traffic_Light_Cars"][1]["Bus_2"] + \
                                        json_data["Traffic_Light_Cars"][1]["Truck_2"]),
        'cnt_emergency_1' : json_data["Traffic_Light_Cars"][0]["Firetruck_1"] + \
                            json_data["Traffic_Light_Cars"][0]["Ambulance_1"], 
        'cnt_emergency_2' : json_data["Traffic_Light_Cars"][1]["Firetruck_2"] + \
                            json_data["Traffic_Light_Cars"][1]["Ambulance_2"]
        }
    update_lights_people = {
        'cnt_people': json_data["Traffic_Light_People"][0]["People"],
        'cnt_silver': json_data["Traffic_Light_People"][0]["Silver"],
        'cnt_wheel': json_data["Traffic_Light_People"][0]["Wheelchair"]
        }
    
    flag_lights_car = json_data["flag_lights_on"][0]["lights_car"]
    if flag_lights_car == "True":
        flag_lights_car = True
    elif flag_lights_car == " False":
        flag_lights_car = False
    flag_lights_ppl = json_data["flag_lights_on"][0]["lights_people"]
    if flag_lights_ppl == "True":
        flag_lights_ppl = True
    elif flag_lights_ppl == " False":
        flag_lights_ppl = False
    data_lights_flag_ud = {
        'flag_lights_car' : flag_lights_car,
        'flag_lights_people' : flag_lights_ppl
        }
    
    return update_lights_car, update_lights_people, data_lights_flag_ud

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
    cnt_emergency_1 = data_lights_car_ff['cnt_emergency_1']
    cnt_emergency_2 = data_lights_car_ff['cnt_emergency_2']
    cnt_silver = data_lights_people_ff['cnt_silver']
    cnt_wheel = data_lights_people_ff['cnt_wheel']
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
                               data_lights_flag_run,
                               data_specific_flag_run
                               ):
    # 기준 시간 재정의
    standard_time_car_r = 30  # 차량용 신호등 적색등 점등 기준 시간
    standard_time_car_y = 3  # 차량용 신호등 황색등 점등 기준 시간
    standard_time_car_g_left = 20  # 차량용 신호등 좌회전등 점등 기준 시간
    standard_time_car_g_straight = 50  # 차량용 신호등 녹색등 점등 기준 시간
    standard_time_peo_g = 30  # 보행자용 신호등 녹색등 점등 기준 시간
    
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
    flag_lights_on_car_run = data_lights_flag_run['flag_lights_car']
    flag_lights_on_ppl_run = data_lights_flag_run['flag_lights_people']

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
            if cnt_straight > cnt_left:  # 직진 차량이 좌회전 차량보다 많을 경우
                t_car_g_s_run = t_car_g_s_run + t_var_car_run  # 직진 신호 시간 증가
            elif cnt_straight < cnt_left:  # 좌회전 차량이 직진 차량보다 많을 경우
                t_car_g_l_run = t_car_g_l_run + t_var_car_run  # 좌회전 신호 시간 증가
        # 인도가 차도보다 복잡한 경우 - 사람 수가 차량 수보다 많을 경우
        elif cnt_total_cars < cnt_total_peo:
            if cnt_total_peo >= 3:  # 이 제어를 해야하나 안 해야하나? 테스트를 통해 확인 필요
                t_car_g_s_run = t_car_g_s_run - t_var_car_run  # 직진 신호 시간 감소
                t_car_g_l_run = t_car_g_l_run - t_var_car_run  # 좌회전 신호 시간 감소
    
    result_lights_time_run = {     
        'standard_time_car_r': standard_time_car_r, 't_car_r': t_car_r_run,
        'standard_time_car_y': standard_time_car_y, 't_car_y': t_car_y_run,
        'standard_time_car_g_left': standard_time_car_g_left, 't_car_g_l': t_car_g_l_run,
        'standard_time_car_g_straight': standard_time_car_g_straight, 't_car_g_s': t_car_g_s_run,
        'standard_time_peo_g': standard_time_peo_g, 't_pple_g': t_pple_g_run
    }
    result_flag_run = {
        'flag_emergency' : flag_car_run, 
        'flag_silver' : flag_people_run, 
        'flag_lights_on_car' : flag_lights_on_car_run, 
        'flag_lights_on_ppl' : flag_lights_on_ppl_run
    }
    
    return result_lights_time_run, result_flag_run

# 메인함수
def main():
    # LED configuration.
    LED_CHANNEL = 0
    LED_COUNT = 33              # How many LEDs to light.
    LED_CNT_R = 9               # How many LEDs to red signal light.
    LED_CNT_G = 9               # How many LEDs to green signal light.
    LED_CNT_Y = 9               # How many LEDs to yellow signal light.
    LED_CNT_LEFT = 6            # How many LEDs to left signal light.
    # LED_CNT_CLEAR = 0           # clear LED
    LED_FREQ_HZ = 800000        # Frequency of the LED signal.  Should be 800khz or 400khz.
    LED_DMA_NUM = 10            # DMA channel to use, can be 0-14.
    LED_GPIO = 18               # GPIO connected to the LED signal line.  Must support PWM!
    LED_BRIGHTNESS = 255        # Set to 0 for darkest and 255 for brightest
    LED_INVERT = 0              # Set to 1 to invert the LED signal, good if using NPN

    DOT_COLORS = [0x008800,   # red
                  0x888800,   # yellow
                  0x880000,	  # green
                  0x000000,   # clear
                  0x200000]	  # test-green


    # Create a ws2811_t structure from the LED configuration.
    leds = ws.new_ws2811_t()

    # Initialize all channels to off
    for channum in range(2):
        channel = ws.ws2811_channel_get(leds, channum)
        ws.ws2811_channel_t_count_set(channel, 0)
        ws.ws2811_channel_t_gpionum_set(channel, 0)
        ws.ws2811_channel_t_invert_set(channel, 0)
        ws.ws2811_channel_t_brightness_set(channel, 0)

    channel = ws.ws2811_channel_get(leds, LED_CHANNEL)

    ws.ws2811_channel_t_count_set(channel, LED_COUNT)
    ws.ws2811_channel_t_gpionum_set(channel, LED_GPIO)
    ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
    ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)

    ws.ws2811_t_freq_set(leds, LED_FREQ_HZ)
    ws.ws2811_t_dmanum_set(leds, LED_DMA_NUM)

    # Initialize library with LED configuration.
    resp = ws.ws2811_init(leds)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))
    
    # 신호등 데이터 정제
    data_lights_time, data_lights_hyper_parameter, data_specific_flag = init_data() 
    num_cycle = 1
    update_data_lights_flag = {
        'update_car_lights_flag' : data_specific_flag['flag_lights_on_car'],
        'update_people_lights_flag' : data_specific_flag['flag_lights_on_ppl']
        }
    
    try:  # 이 try 안의 구문을 먼저 수행하고
        LED_mode = 0 # 0 Clear / 1 Red / 2 Yellow / 3 Green left / 4 Green straight
        while True:  # 무한루프 시작: 아두이노의 loop()와 같음
            
            # 신호등 데이터 갱신
            update_data_car, update_data_people, update_data_lights_flag = \
                update_data(update_data_lights_flag)
            
            ###################################################################
            # 1. 차량의 정지 & 보행자의 횡단
            # 신호등 제어 동작 함수 - # 변동 시간 적용
            result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                         update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                         data_lights_time,  # 신호 패턴 시간 데이터
                                                                         data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                         update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                         data_specific_flag) # 특수 상황에 대한 신호 데이터
            data_lights_time = result_lights_time
            data_specific_flag = result_flag
            
            # 모든 LED reset(clear)
            num_led = 0 # 해당값부터 LED_COUNT까지 점등
            for i in range(LED_COUNT):
                color = DOT_COLORS[3]
                # Set the LED color buffer value.
                ws.ws2811_led_set(channel, num_led + i, color)  
            # Send the LED color data to the hardware.
            resp = ws.ws2811_render(leds)
            # LED red
            LED_mode = 1
            if LED_mode == 1:
                num_led = 0 # 해당값부터 LED_COUNT까지 점등
                for i in range(LED_CNT_R):
                    color = DOT_COLORS[3]
                    color = DOT_COLORS[0]   
                    # Set the LED color buffer value.
                    ws.ws2811_led_set(channel, num_led + i, color)
                # Send the LED color data to the hardware.
                resp = ws.ws2811_render(leds)
            
            # 차량 정지 & 보행자 횡단
            pattern_time = result_lights_time['t_pple_g']
            if result_flag['flag_silver'] == True and result_flag['flag_lights_on_ppl'] == True: # 특수상황
                while pattern_time != 0:
                    # 신호등 데이터 갱신
                    update_data_car, update_data_people, update_data_lights_flag = \
                        update_data(update_data_lights_flag)
                        
                    result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                                 update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                                 data_lights_time,  # 신호 패턴 시간 데이터
                                                                                 data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                                 update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                                 data_specific_flag) # 특수 상황에 대한 신호 데이터
                    data_lights_time = result_lights_time
                    data_specific_flag = result_flag
                    data_flag = result_flag['flag_silver']
                    if data_flag == True and pattern_time <= 5:
                        pattern_time = 5
                    print(pattern_time)
                    pattern_time = pattern_time - 1
                    time.sleep(1)
            else: # 평시
                while pattern_time != 0:
                    # 신호등 데이터 갱신
                    update_data_car, update_data_people, update_data_lights_flag = \
                        update_data(update_data_lights_flag)
                    result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                                 update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                                 data_lights_time,  # 신호 패턴 시간 데이터
                                                                                 data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                                 update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                                 data_specific_flag) # 특수 상황에 대한 신호 데이터
                    data_lights_time = result_lights_time
                    data_specific_flag = result_flag
                    data_flag = result_flag['flag_silver']
                    if data_flag == True and pattern_time <= 5: # 평시였다가 특수상황의 발생 경우
                        pattern_time = 5
                    print(pattern_time)
                    pattern_time = pattern_time - 1
                    time.sleep(1)
            ###################################################################
            # 2. 차량의 직진 & 보행자의 대기
            # 신호등 데이터 갱신
            update_data_car, update_data_people, update_data_lights_flag = \
                update_data(update_data_lights_flag)
                
            result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                         update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                         data_lights_time,  # 신호 패턴 시간 데이터
                                                                         data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                         update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                         data_specific_flag) # 특수 상황에 대한 신호 데이터
            data_lights_time = result_lights_time
            data_specific_flag = result_flag
            
            # 모든 LED reset(clear)
            num_led = 0 # 해당값부터 LED_COUNT까지 점등
            for i in range(LED_COUNT):
                color = DOT_COLORS[3]
                # Set the LED color buffer value.
                ws.ws2811_led_set(channel, num_led + i, color)  
            # Send the LED color data to the hardware.
            resp = ws.ws2811_render(leds)
            # LED green straight
            LED_mode = 4
            if LED_mode == 4:
                num_led = LED_CNT_R + LED_CNT_Y + LED_CNT_LEFT # 해당값부터 LED_COUNT까지 점등
                for i in range(LED_CNT_G):
                    color = DOT_COLORS[3]
                    color = DOT_COLORS[2]
                    # Set the LED color buffer value.
                    ws.ws2811_led_set(channel, num_led + i, color)
                # Send the LED color data to the hardware.
                resp = ws.ws2811_render(leds)
                
            # 차량 직진!
            pattern_time = result_lights_time['t_car_g_s']
            if result_flag['flag_emergency'] == True and result_flag['flag_lights_on_car'] == True: # 특수상황
                while pattern_time != 0:
                    # 신호등 데이터 갱신
                    update_data_car, update_data_people, update_data_lights_flag = \
                        update_data(update_data_lights_flag)
                        
                    result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                                 update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                                 data_lights_time,  # 신호 패턴 시간 데이터
                                                                                 data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                                 update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                                 data_specific_flag) # 특수 상황에 대한 신호 데이터
                    data_lights_time = result_lights_time
                    data_specific_flag = result_flag
                    data_flag = result_flag['flag_emergency']
                    if data_flag == True and pattern_time <= 5:
                        pattern_time = 5
                    print(pattern_time)
                    pattern_time = pattern_time - 1
                    time.sleep(1)
            else: # 평시
                while pattern_time != 0:
                    # 신호등 데이터 갱신
                    update_data_car, update_data_people, update_data_lights_flag = \
                        update_data(update_data_lights_flag)
                        
                    result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                                 update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                                 data_lights_time,  # 신호 패턴 시간 데이터
                                                                                 data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                                 update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                                 data_specific_flag) # 특수 상황에 대한 신호 데이터
                    data_lights_time = result_lights_time
                    data_specific_flag = result_flag
                    data_flag = result_flag['flag_emergency']
                    if data_flag == True and pattern_time <= 5: # 평시였다가 특수상황의 발생 경우
                        pattern_time = 5
                    print(pattern_time)
                    pattern_time = pattern_time - 1
                    time.sleep(1)
                    
            ###################################################################
            # 2-1. 황색등 점멸
            # 모든 LED reset(clear)
            num_led = 0 # 해당값부터 LED_COUNT까지 점등
            for i in range(LED_COUNT):
                color = DOT_COLORS[3]
                # Set the LED color buffer value.
                ws.ws2811_led_set(channel, num_led + i, color)  
            # Send the LED color data to the hardware.
            resp = ws.ws2811_render(leds)
            # LED yello
            LED_mode = 2
            if LED_mode == 2:
                num_led = LED_CNT_R # 해당값부터 LED_COUNT까지 점등
                for i in range(LED_CNT_Y):
                    color = DOT_COLORS[3]
                    color = DOT_COLORS[1]
                    # Set the LED color buffer value.
                    ws.ws2811_led_set(channel, num_led + i, color)
                # Send the LED color data to the hardware.
                resp = ws.ws2811_render(leds)

            # 차량 대기 & 보행자 대기
            pattern_time = result_lights_time['t_car_y']
            while pattern_time != 0:
                print(pattern_time)
                pattern_time = pattern_time-1
                time.sleep(1)
            ###################################################################
            # 3. 차량의 좌회전 & 보행자의 대기
            # 신호등 데이터 갱신
            update_data_car, update_data_people, update_data_lights_flag = \
                update_data(update_data_lights_flag)
                
            result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                         update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                         data_lights_time,  # 신호 패턴 시간 데이터
                                                                         data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                         update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                         data_specific_flag) # 특수 상황에 대한 신호 데이터
            data_lights_time = result_lights_time
            data_specific_flag = result_flag
            
            # 모든 LED reset(clear)
            num_led = 0 # 해당값부터 LED_COUNT까지 점등
            for i in range(LED_COUNT):
                color = DOT_COLORS[3]
                # Set the LED color buffer value.
                ws.ws2811_led_set(channel, num_led + i, color)  
            # Send the LED color data to the hardware.
            resp = ws.ws2811_render(leds)
            # LED green left
            LED_mode = 3
            if LED_mode == 3:
                num_led = LED_CNT_R + LED_CNT_Y # 해당값부터 LED_COUNT까지 점등
                for i in range(LED_CNT_LEFT):
                    color = DOT_COLORS[3]
                    color = DOT_COLORS[2]
                    # Set the LED color buffer value.
                    ws.ws2811_led_set(channel, num_led + i, color)
                # Send the LED color data to the hardware.
                resp = ws.ws2811_render(leds)
                
            # 차량 좌회전!
            pattern_time = result_lights_time['t_car_g_l']
            if result_flag['flag_emergency'] == True and result_flag['flag_lights_on_car'] == True: # 특수상황
                while pattern_time != 0:
                    # 신호등 데이터 갱신
                    update_data_car, update_data_people, update_data_lights_flag = \
                        update_data(update_data_lights_flag)
                        
                    result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                                 update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                                 data_lights_time,  # 신호 패턴 시간 데이터
                                                                                 data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                                 update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                                 data_specific_flag) # 특수 상황에 대한 신호 데이터
                    data_lights_time = result_lights_time
                    data_specific_flag = result_flag
                    data_flag = result_flag['flag_emergency']
                    if data_flag == True and pattern_time <= 3:
                        pattern_time = 3
                    print(pattern_time)
                    pattern_time = pattern_time-1
                    time.sleep(1)
            else: # 평시
                while pattern_time != 0:
                    # 신호등 데이터 갱신
                    update_data_car, update_data_people, update_data_lights_flag = \
                        update_data(update_data_lights_flag)
                        
                    result_lights_time, result_flag = run_control_traffic_lights(update_data_car,  # 차량용 신호등 클래스 카운트 데이터
                                                                                 update_data_people,  # 보행자용용 신호등 클래스 카운트 데이터
                                                                                 data_lights_time,  # 신호 패턴 시간 데이터
                                                                                 data_lights_hyper_parameter,  # 패턴 변동 시간, 차량 가중치 등 하이퍼-파라미터
                                                                                 update_data_lights_flag, # 신호등 점등 신호 데이터
                                                                                 data_specific_flag) # 특수 상황에 대한 신호 데이터
                    data_lights_time = result_lights_time
                    data_specific_flag = result_flag
                    data_flag = result_flag['flag_emergency']
                    if data_flag == True and pattern_time <= 3: # 평시였다가 특수상황의 발생 경우
                        pattern_time = 3
                    print(pattern_time)
                    pattern_time = pattern_time - 1
                    time.sleep(1)
            ###################################################################
            # 3-1. 황색등 점멸
            # 모든 LED reset(clear)
            num_led = 0 # 해당값부터 LED_COUNT까지 점등
            for i in range(LED_COUNT):
                color = DOT_COLORS[3]
                # Set the LED color buffer value.
                ws.ws2811_led_set(channel, num_led + i, color)  
            # Send the LED color data to the hardware.
            resp = ws.ws2811_render(leds)
            # LED yello & green left
            LED_mode = 2
            if LED_mode == 2:
                # LED yellow
                num_led = LED_CNT_R # 해당값부터 LED_COUNT까지 점등
                for i in range(LED_CNT_Y):
                    color = DOT_COLORS[3]
                    color = DOT_COLORS[1]
                    # Set the LED color buffer value.
                    ws.ws2811_led_set(channel, num_led + i, color)
                    # LED green left
                num_led = LED_CNT_R + LED_CNT_Y # 해당값부터 LED_COUNT까지 점등
                for i in range(LED_CNT_LEFT):
                    color = DOT_COLORS[3]
                    color = DOT_COLORS[2]
                    # Set the LED color buffer value.
                    ws.ws2811_led_set(channel, num_led + i, color)
                    
                # Send the LED color data to the hardware.
                resp = ws.ws2811_render(leds)
            
            # 차량 대기 & 보행자 대기
            pattern_time = result_lights_time['t_car_y']
            while pattern_time != 0:
                print(pattern_time)
                pattern_time = pattern_time-1
                time.sleep(1)

            # 제어 전 출력 테스트
            print("# 신호등 1주기를 주기로 신호 패턴 시간 출력")
            print(str(num_cycle) + "주기")
            num_cycle = num_cycle + 1
            print("차_적", result_lights_time['t_car_r'])
            print("차_황", result_lights_time['t_car_y'])
            print("차_초_좌", result_lights_time['t_car_g_l'])
            print("차_초_직", result_lights_time['t_car_g_s'])
            print("사_초", result_lights_time['t_pple_g'])
            print("")
            
    # 이부분은 반드시 추가해주셔야 합니다.
    finally:  # try 구문이 종료되면
        pass
        ws.ws2811_fini(leds)
        ws.delete_ws2811_t(leds)

# 파일 실행 시점
if __name__ == "__main__":
    main()
