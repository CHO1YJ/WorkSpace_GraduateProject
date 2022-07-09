import logging
import json
import paho.mqtt.client as mqtt                                                                # (1)


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Global Variables                                                                 # (2)
BROKER_PORT = 1883
CLIENT_ID = "LEDClient"                                                                         # (3)
TOPIC = "traffic_data"                                                                          # (4)
client = None  # MQTT client instance. See init_mqtt()                                          # (5)
json_data = None

count_car_1 = 0
count_car_2 = 0
count_bus_1 = 0
count_bus_2 = 0
count_emergency_1 = 0
count_emergency_2 = 0
data_traffic_lights_car = {}

count_people = 0
count_wheel = 0
data_traffic_lights_people = {}

def set_traffic_data(data):                                                                       # (6)
    json_data = json.loads(data)
    # Traffic_Light_Cars 정보를 조회
    print(json_data["Traffic_Light_Cars"])
    # Traffic_Light_People 정보를 조회 -> 0번째 배열의 Wheelchair key를 통해 value에 접근
    print("사람으로 확인되는 인원은 " + \
          str(json_data["Traffic_Light_People"][0]["People"]) \
          + "명 입니다.")
    print("휠체어를 탄 것으로 확인되는 인원은 " + \
          str(json_data["Traffic_Light_People"][0]["Wheelchair"]) \
          + "명 입니다.")
    print("노약자로 확인되는 인원은 " + \
          str(json_data["Traffic_Light_People"][0]["Silver"]) \
          + "명 입니다.")
    # 데이터 전체 구조 출력
    print(json.dumps(json_data, indent="\t"))

    count_car_1 = json_data["Traffic_Light_People"][0]["Car_left"]
    count_car_2 = json_data["Traffic_Light_People"][0]["Car_straight"]
    count_bus_1 = json_data["Traffic_Light_People"][0]["Truck_left"]
    count_bus_2 = json_data["Traffic_Light_People"][0]["Truck_straight"]
    count_emergency_1 = json_data["Traffic_Light_People"][0]["Firetruck_left"] + json_data["Traffic_Light_People"][0]["Ambulance_left"]
    count_emergency_2 = json_data["Traffic_Light_People"][0]["Firetruck_straight"] + json_data["Traffic_Light_People"][0]["Ambulance_straight"]

    data_traffic_lights_car = {
        'count_car_1': count_car_1,
        'count_car_2': count_car_2,
        'count_bus_1': count_bus_1,
        'count_bus_2': count_bus_2,
        'count_emergency_1': count_emergency_1,
        'count_emergency_2': count_emergency_2,
    }

    count_people = json_data["Traffic_Light_People"][0]["People"]  # 보행자 카운트
    count_wheel = json_data["Traffic_Light_People"][0]["Wheelchair"]  # 휠체어 카운트
    
    data_traffic_lights_people = {
        'count_people': count_people,
        'count_wheel': count_wheel,
    }

"""
MQTT Related Functions and Callbacks
"""
def on_connect(client, user_data, flags, connection_result_code):                              # (7)
    """on_connect is called when our program connects to the MQTT Broker.
       Always subscribe to topics in an on_connect() callback.
       This way if a connection is lost, the automatic
       re-connection will also results in the re-subscription occurring."""

    if connection_result_code == 0:                                                            # (8)
        # 0 = successful connection
        logger.info("Connected to MQTT Broker")
    else:
        # connack_string() gives us a user friendly string for a connection code.
        logger.error("Failed to connect to MQTT Broker: " + mqtt.connack_string(connection_result_code))

    # Subscribe to the topic for LED level changes.
    client.subscribe(TOPIC, qos=2)                                                             # (9)



def on_disconnect(client, user_data, disconnection_result_code):                               # (10)
    """Called disconnects from MQTT Broker."""
    logger.error("Disconnected from MQTT Broker")


def on_message(client, userdata, msg):                                                         # (11)
    """Callback called when a message is received on a subscribed topic."""
    logger.debug("Received message for topic {}: {}".format(msg.topic, msg.payload))

    try:
        data = str(msg.payload.decode("UTF-8"))         # (12)
    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: " + msg.payload.decode("UTF-8"))

    if msg.topic == TOPIC:                                                                     # (13)
        set_traffic_data(data)                                                                    # (14)
    else:
        logger.error("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))

def init_mqtt():
    global client

    # Our MQTT Client. See PAHO documentation for all configurable options.
    # "clean_session=True" means we don"t want Broker to retain QoS 1 and 2 messages
    # for us when we"re offline. You"ll see the "{"session present": 0}" logged when
    # connected.
    client = mqtt.Client()

    # Route Paho logging to Python logging.                                                      # (16)
    client.enable_logger()

    # Setup callbacks
    client.on_connect = on_connect                                                             # (17)
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to Broker.
    client.connect('3.35.210.63', 1883)                                                   # (18)

# Initialise Module
init_mqtt()

if __name__ == "__main__":                    # (19)
    logger.info("Listening for messages on topic '" + TOPIC + "'. Press Control + C to exit.")

    client.loop_forever()                                                                        # (20)