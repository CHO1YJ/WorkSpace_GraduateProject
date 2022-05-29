import RPi.GPIO as GPIO     # 라즈베리파이 GPIO 관련 모듈을 불러옴
import time                 # 시간관련 모듈을 불러옴

GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정

### 이부분은 아두이노 코딩의 setup()에 해당합니다
LED_pin_R = 2                     # LED 핀은 라즈베리파이 GPIO 2번핀으로
GPIO.setup(LED_pin_R, GPIO.OUT)   # LED 핀을 출력으로 설정

LED_pin_Y = 3                     # LED 핀은 라즈베리파이 GPIO 2번핀으로
GPIO.setup(LED_pin_Y, GPIO.OUT)   # LED 핀을 출력으로 설정

LED_pin_G_S = 4                     # LED 핀은 라즈베리파이 GPIO 2번핀으로
GPIO.setup(LED_pin_G_S, GPIO.OUT)   # LED 핀을 출력으로 설정

LED_pin_G_L = 5                    # LED 핀은 라즈베리파이 GPIO 2번핀으로
GPIO.setup(LED_pin_G_L, GPIO.OUT)   # LED 핀을 출력으로 설정

###############################################################################
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

count_people = 5 # 보행자 카운트
count_silver = 0 # 노약자 카운트
count_wheel = 0 # 휠체어 카운트

# 신호등 패턴 조절 함수의 변수 설정 
# 차량용 보행자용 총 시간은 각각 60초로 기준 설정
time_car_r = 28 # 차량용 신호등 적색등 점등 시간
time_car_y = 4 # 차량용 신호등 황색등 점등 시간
time_car_g_left = 14 # 차량용 신호등 좌회전등 점등 시간; 직진 신호랑 겹침
time_car_g_stright = 28 # 차량용 신호등 녹색등 점등 시간
# time_peo_r = 28 # 보행자용 신호등 적색등 점등 시간
time_peo_g = 28 # 보행자용 신호등 녹색등 점등 시간

weight_bus = 2 # 크기로 볼 때, 일반 차량의 2배로 생각
# 시간 변화량 정의
t_var_car = 1
t_var_pple = 1
###############################################################################

###############################################################################
def Control_Traffic_Lights_by(cnt_car1, cnt_car2, cnt_car3, \
                                  cnt_bus1, cnt_bus2, cnt_bus3,
                                  cnt_emgncy1, cnt_emgncy2, cnt_emgncy3, \
                                      cnt_pple):
    # 직진 및 좌회전 시의 차량 및 구급차, 소방차 대수 계산
    cnt_left = cnt_car1 + cnt_bus1 * weight_bus
    cnt_straight = cnt_car2 + cnt_car3 + (cnt_bus2 + cnt_bus3) * weight_bus
    cnt_emgncy_left = cnt_emgncy1
    cnt_emgncy_straight = cnt_emgncy2 + cnt_emgncy3
    # 횡단보도에서 인식된 사람들 및 노약자와 휠체어 수 계산
    cnt_total_peo = count_people + count_silver + count_wheel
    cnt_sil = count_silver
    cnt_whl = count_wheel
    
    flag_emergency = False # 구급차, 소방차 인식되면 True / 평시 False
    flag_silver = False # 노약자 및 휠체어가 인식되면 True / 평시 False
    
    t_car_g_stright = time_car_g_stright
    t_car_g_left = time_car_g_left
    t_car_r = time_car_r
    t_peo_g = time_peo_g
    # t_peo_r = t_car_g_stright + t_car_g_left + time_car_y
    
    # 차량 신호등 제어
    # 긴급 상황 발생
    if cnt_emgncy_straight > 0 or cnt_emgncy_left > 0:
        flag_emergency = True
    # 평시
    if flag_emergency == False:
        if 16 <= t_car_g_stright <= 40 or 7 <= t_car_g_left <= 26:   
            if cnt_straight >= cnt_left:
                t_car_g_stright = time_car_g_stright + t_var_car
                t_car_g_left = time_car_g_left - t_var_car   
            elif cnt_straight < cnt_left:
                t_car_g_stright = time_car_g_stright - t_var_car
                t_car_g_left = time_car_g_left - t_var_car
            temp_t_car_g_strit = t_car_g_stright
            temp_t_car_g_lft = t_car_g_left
        t_car_g_stright = temp_t_car_g_strit
        t_car_g_left = temp_t_car_g_lft
    # 긴급 상황 시
    if flag_emergency == True:
        if cnt_emgncy_straight > 0:
            t_car_g_stright = 60
            t_car_g_left = 60
        elif cnt_emgncy_left > 0:
            t_car_g_stright = 60
            t_car_g_left = 60   
        flag_emergency = False
        
    # 보행자 신호등 제어
    # 노약자 및 휠체어 인식
    if cnt_sil > 0 or cnt_whl > 0:
        flag_silver = True
    # 평시
    if flag_silver == False:    
        t_car_r = 28
        t_peo_g = 28
        if 16 <= t_car_g_stright <= 40 or 7 <= t_car_g_left <= 26:   
            if cnt_total_peo >= 5:
                t_car_g_stright = time_car_g_stright - t_var_car
                t_car_g_left = time_car_g_left - t_var_car   
            elif cnt_total_peo < 5:
                t_car_g_stright = time_car_g_stright + t_var_car
                t_car_g_left = time_car_g_left + t_var_car  
            temp_t_car_g_strit = t_car_g_stright
            temp_t_car_g_lft = t_car_g_left
        t_car_g_stright = temp_t_car_g_strit
        t_car_g_left = temp_t_car_g_lft
    # 노약자 및 휠체어 인식
    if flag_silver == True:
        t_car_r = t_car_r + 10
        t_peo_g = t_peo_g + 10
        flag_silver = False

    return t_car_g_stright, t_car_g_left, t_car_r, t_peo_g # 차량 신호등 직진 좌회전 시간 제어

###############################################################################


### 이부분은 아두이노 코딩의 loop()에 해당합니다
try:                                        # 이 try 안의 구문을 먼저 수행하고
    while True:                             # 무한루프 시작: 아두이노의 loop()와 같음
    
        # 신호등 제어 함수 호출
        time_car_g_stright, time_car_g_left, time_car_r, t_peo_g = \
            Control_Traffic_Lights_by(count_car_1, count_car_2, count_car_3, \
                                      count_bus_1, count_bus_2, count_bus_3, \
                                          count_emergency_1, count_emergency_2, \
                                              count_emergency_3, count_people)
    
        # 1. 차량 정지 & 보행자 횡단 적용 + 추후 긴급상황과 노약자 및 휠체어 경우도 적용 필요!
        GPIO.output(LED_pin_R, GPIO.HIGH)   # 적색등 On
        GPIO.output(LED_pin_Y, GPIO.LOW)    # 황색등 Off
        GPIO.output(LED_pin_G_S, GPIO.LOW)  # 녹색 직진등 Off
        GPIO.output(LED_pin_G_L, GPIO.LOW)  # 녹색 좌회전등 Off
        time.sleep(time_car_r)              # 차량 정지 & 보행자 횡단
        GPIO.output(LED_pin_Y, GPIO.HIGH)   # 황색등 On - 신호 변경 준비
        time.sleep(time_car_y)              # 황색등 - 과도기 : 4초간 대기
        # 2. 차량 통행 & 보행자 대기 + 추후 긴급상황 경우도 적용 필요!
        GPIO.output(LED_pin_R, GPIO.LOW)    # 적색등 Off
        GPIO.output(LED_pin_Y, GPIO.LOW)    # 황색등 Off
        GPIO.output(LED_pin_G_S, GPIO.HIGH) # 녹색 직진등 On
        GPIO.output(LED_pin_G_L, GPIO.HIGH) # 녹색 좌회전등 On
        time.sleep(time_car_g_left)         # 차량 직진 + 좌회전!
        GPIO.output(LED_pin_G_L, GPIO.LOW)  # 녹색 좌회전등 Off
        time.sleep(time_car_g_stright - time_car_g_left) # 차량 직진!

    ### 이부분은 반드시 추가해주셔야 합니다.
finally:                                # try 구문이 종료되면
    GPIO.cleanup()                      # GPIO 핀들을 초기화
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    