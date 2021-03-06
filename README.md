# 1. Control Patterns of Traffic Lights

## 1.1 신호등 패턴의 개발 배경 및 경과

21년 말부터 시작된 졸업작품의 아이디어 회의 끝에 올해 1월에 AI를 이용한 신호등 제어시스템을 기획하게 되었다. 다음 라즈베리파이 부에서는 AWS를 통해 전달받고 YOLOv5에 의하여 인식된 차량의 수 및 사람의 수의 값들을 MQTT를 이용하여 받아올 예정이다. 이번에는 받아온 값들을 기반하여 크게 자동차의 직진과 좌회전 그리고 사람이 횡단보도를 건너는 것의 여부를 제어하는 것을, 세부적으로는 소방차, 구급차에 대한 긴급 상황과 노약자와 휠체어가 인식된 경우까지 감안하여 코딩해 볼 수 있었다.

![image](https://user-images.githubusercontent.com/103302903/170281334-1c2e964b-f2ed-4c64-815e-359cd93feff7.png)

## 1.2 신호등 제어 알고리즘 설명

#### 전제 및 가정사항
- 대전제 : 해당 프로그램은 4차선(1차선 : 좌회전 차선, 2차선 : 직진 차선) 삼거리의 상황이라고 가정한다.

#### 신호의 순서
1. 보행자 신호 - 사람들의 횡단보도 횡단; 적색등 On / 황색등, 좌회전등, 녹색등 Off
2. 차량 신호 - 차량의 직진; 적색등, 황색등, 좌회전등 Off / 녹색등 On
3. 차량 신호 - 차량의 좌회전; 적색등, 황색등, 녹색등 Off / 좌회전등 On
4. 대기 신호 - 사람들과 차량의 대기(신호 변경 대비); 적색등, 녹색등 Off / 좌회전등, 황색등 On

#### 카운트 계산
1. 1차선의 차량은 좌회전 차량으로 카운트 계산
2. 2차선의 차량은 직진 차량으로 카운트 계산
3. 1차선, 2차선에서 인식된 차량의 가중치 1을 기준으로 버스 및 트럭의 가중치는 2로 설정 - 일반적으로 차량이 도로를 차지하는 면적을 약 2배로 생각
4. 소방차, 구급차에 대해 직진, 좌회전 차량 카운트 인식 - **긴급 상황을 대비**
5. 일반인, 휠체어, 노인의 인식의 합을 전체 보행자로 카운트 계산
6. 노인에 대해 카운트 계산 - **긴급 상황을 대비**
7. 휠체어에 대해 카운트 계산 - **긴급 상황을 대비**

#### 긴급상황 플래그
1. 차량용 신호등 플래그 - 구급차, 소방차 인식 시 플래그 On
2. 보행자용 신호등 플래그 - 노인, 휠체어 인식 시 플래그 On

#### 한계값 및 시간 통제 정의
1. 직진 : 50초 / 죄회전 : 20초 / 정지 : 30초 / 과도기(황색등) : 3초 - **추후에 변동시켜야 하는 값**
2. 모든 시간은 다음을 따른다. : 0.5 * 시간 < 시간 < 1.5 * 시간
3. 차량용 신호등 긴급 상황 시에는 시간이 감소하다가 긴급 상황의 해제 전까지 특정 시간에서 정지
4. 보행자용 신호등 긴급 상황 시에는 시간이 감소하다가 긴급 상황의 해제 전까지 특정 시간에서 정지
4-1. 대안으로 인식이 계속될 경우 1초에서 정지하는 것도 고려(해당 부분을 적용 완료)

#### 차량용 신호등 작동 알고리즘
1. "사람의 수"와 "차량의 수"를 비교
2. "직진 차선 차량 수"와 "좌회전 차선 차량 수"를 비교
3. 시간을 조정한 후 직진 및 좌회전 신호 패턴 시간을 진행
4. 긴급 상황 시에는 좌회전 신호의 경우 3초에서 정지, 직진 신호의 경우 5초에서 정지

#### 보행자용 신호등 작동 알고리즘
1. "사람의 수"와 "차량의 수"를 비교
2. 보행자 횡단 신호 패턴 시간을 진행
3. 긴급 상황 시에는 보행자 횡단 신호의 경우 5초에서 정지

#### 신호등 시간 측정 방식 변경
- "한계값 및 시간 통제 정의"에서 4-1을 충족시키기 위해서는 시간을 1초 단위로 쪼개서 관리할 필요성이 존재

변경 전; 시간의 어느 시각을 통제 불능

    time.sleep('t_car_y')

변경 후; 시간의 어느 시각을 통제 가능

    GPIO.output(LED_pin_Y, GPIO.HIGH)  # 신호(ex; 황색등 On - 신호 변경 준비)
    # 신호에 따른 차량과 사람의 행동(ex; 차량 대기 & 보행자 대기)
    pattern_time = result_lights_time['t_car_y']
    while pattern_time != 0:
        print(pattern_time)
        pattern_time = pattern_time-1
        time.sleep(1)

#### 하드웨어부 필수 코드 안내
회로 보호를 위한 코드

    finally:                            # try 구문이 종료되면
    GPIO.cleanup()                      # GPIO 핀들을 초기화

## 1.3 MQTT(Message Queue Telemetry Transport)
- AWS 서버에서 MQTT를 통해 JSON 파일 형식으로 라즈베리파이로 데이터를 받아와 신호 패턴을 최적화한다.

##### JSON 파일 형식 - "Key" : value
예시)

    {
        "Traffic_Light_Cars" : [{
            "Cars"      : 6,
            "Bus"       : 1,
            "Truck"     : 1,
            "Firetruck" : 0,
            "Ambulance" : 0
        }],
        "Traffic_Light_People" : [{
            "People"        : 4,
            "Wheelchair"    : 1,
            "Silver"        : 0
        }]
    }

## 1.4 개발 완료
1. 이미지 데이터를 입력으로 하여 좌표값을 추출해 내는 알고리즘의 작성을 완료했다.
2. 영상 데이터의 경우에는 바로 입력으로 사용이 불가하여 frame 단위로 영상을 이미지로 분리하는 알고리즘의 작성을 완료했다.
3. YOLOv5 파일에서 추출한 좌표값을 통해 카운트 구역을 설정하고 설정된 구역에서 차량 및 사람을 카운트하는 것을 완료했다.
4. vdo_data.py 파일에서 영상 데이터를 1장만 저장이 되도록 수정을 완료했다.
5. 테스트용 json 파일을 생성하였고 파이썬을 통해 json 데이터 추출에 성공하였다.
6. 라즈베리를 통해 신호등을 제어하는 코드의 기반을 생성하는데 성공했다.
7. 팀원과 협력하여 neopixel LED strip을 자유롭게 제어하는데 성공했다.
8. 기존의 신호등 제어 알고리즘에 차량 및 사람의 count-data를 받아오기 위해 MQTT를 적용하였고 이를 기반하여 신호등의 기본 동작을 확인하는데 성공했다.

## 1.5 추후 개발 계획
1. 라즈베리끼리 데이터를 공유할 수 있도록 개발할 예정이다.
2. 지속적인 테스트를 통해 신호 패턴의 기준 시간 및 변동 시간의 최적화가 필요로 하다.
3. 현재는 argument를 문자열로 받아와 카운트하는 구역을 그리는데 시간이 된다면 이를 메모장 파일 또는 JSON 파일로 받아와 구역을 그리는 방식으로 변경할 계획이다.

## 1.6 참고 자료
1. neopixel LED strip 제어
- https://nan-sso-gong.tistory.com/6
- https://github.com/rpi-ws281x/rpi-ws281x-python
2. 신호등 제어 알고리즘과 MQTT 알고리즘의 결합
- https://jusths.tistory.com/24
