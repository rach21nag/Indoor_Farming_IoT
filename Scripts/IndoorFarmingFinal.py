import threading
import RPi.GPIO as GPIO
import time
import board
import adafruit_dht
from datetime import datetime
import paho.mqtt.publish as publish
import requests
import subprocess
import ast
import paho.mqtt.client as paho

MQTT_SERVER = "192.168.0.100"
SENSOR_TOPIC = "indoor_farm"
PDDL_TOPIC = "indoor_farm_pddl"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24
coil_WA_1_pin = 1
coil_WA_2_pin = 7
coil_WB_1_pin = 8
coil_WB_2_pin = 25

StepCount = 8
Seq = list(range(0, StepCount))
Seq[0] = [1, 0, 0, 0]
Seq[1] = [1, 1, 0, 0]
Seq[2] = [0, 1, 0, 0]
Seq[3] = [0, 1, 1, 0]
Seq[4] = [0, 0, 1, 0]
Seq[5] = [1, 0, 1, 1]
Seq[6] = [0, 0, 0, 1]
Seq[7] = [1, 0, 0, 0]

# GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(coil_WA_1_pin, GPIO.OUT)
GPIO.setup(coil_WA_2_pin, GPIO.OUT)
GPIO.setup(coil_WB_1_pin, GPIO.OUT)
GPIO.setup(coil_WB_2_pin, GPIO.OUT)

# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D2)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT11(board.D2, use_pulseio=False)


# GPIO.output(enable_pin, 1)

def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)


def setStep2(x1, x2, x3, x4):
    GPIO.output(coil_WA_1_pin, x1)
    GPIO.output(coil_WA_2_pin, x2)
    GPIO.output(coil_WB_1_pin, x3)
    GPIO.output(coil_WB_2_pin, x4)


def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


def forward1(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep2(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


def backwards1(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep2(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)


# def readSensorData():
#     global tempSensor
#     global humSensor
#     tempSensor = data
#     humSensor = data1
# 
# 
# def readSensorData1():
#     global ldrSensor
#     ldrSensor = data2
# 
# 
# def readSensorData2():
#     global soilSensor
#     soilSensor = data3


def dht_11():
    payload_data = None
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        if temperature_c > 26:
            print("Temperature is Hot, Temp: {:.1f} C Humidity: {}% ".format(temperature_c, humidity))
            # delay = 50
            # steps = 20
            # forward(int(delay) / 1000.0, int(steps))
        elif temperature_c >= 22 and temperature_c <= 26:
            print("Optimum Temperature, Temp: {:.1f} C Humidity: {}% ".format(temperature_c, humidity))
        else:
            print("Temperature too cold, Temp: {:.1f} C Humidity: {}% ".format(temperature_c, humidity))
            # delay = 50
            # steps = 20
            # backwards(int(delay) / 1000.0, int(steps))
        data_temp = temperature_c
        data_humi = humidity
        payload_data = {}
        payload_data["temperature"] = data_temp
        payload_data["humidity"] = data_humi
        print(f"data_temp : {data_temp}")
        print(f"data_humi : {data_humi}")

        #         readSensorData()
        # payload = str(payload_data)
        # print(payload)
        # print(payload1)
        # publish.single(MQTT_PATH, payload, hostname=MQTT_SERVER)
        # publish.single(MQTT_PATH, payload1, hostname=MQTT_SERVER)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
    return payload_data


def ldr():
    payload_data = None

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    LIGHT_PIN = 27
    GPIO.setup(LIGHT_PIN, GPIO.IN)
    # LED_PIN = 18
    # GPIO.setup(LED_PIN, GPIO.OUT)
    lOld = not GPIO.input(LIGHT_PIN)
    if GPIO.input(LIGHT_PIN) != lOld:
        payload_data = {}
        if GPIO.input(LIGHT_PIN):
            print('\u263e, no light')
            # GPIO.output(LED_PIN, True)
            data_light = GPIO.input(LIGHT_PIN)
            payload_data["light"] = data_light
            print(f"data_light 1 : {data_light}")

            #             readSensorData1()
            # payload2 = str(payload_data)
            # print(payload2)
            # publish.single(MQTT_PATH, payload2, hostname=MQTT_SERVER)
        else:
            print('\u263c, enough light')
            # GPIO.output(LED_PIN, False)
            data_light = GPIO.input(LIGHT_PIN)
            payload_data["light"] = data_light
            print(f"data_light 2 : {data_light}")

            # readSensorData1()
            # payload2 = str(data_light)
            # print(payload2)
            # publish.single(MQTT_PATH, payload2, hostname=MQTT_SERVER)

    lOld = GPIO.input(LIGHT_PIN)
    time.sleep(2.0)
    return payload_data


def soil():
    payload_data = None

    SOIL_PIN = 14
    GPIO.setup(SOIL_PIN, GPIO.IN)
    # LED_SOIL_PIN = 3
    # GPIO.setup(LED_SOIL_PIN, GPIO.OUT)
    soilm = not GPIO.input(SOIL_PIN)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    if GPIO.input(SOIL_PIN) != soilm:
        payload_data = {}

        if GPIO.input(SOIL_PIN):
            print('Water absent')
            data_soil = GPIO.input(SOIL_PIN)
            payload_data["soil"] = data_soil
            print(f"data_soil 1 : {data_soil}")

            # readSensorData2()
            # payload3 = str(data_soil)
            # print(payload3)
            # publish.single(MQTT_PATH, payload3, hostname=MQTT_SERVER)
            # GPIO.output(LED_SOIL_PIN, True)
            # delay = 50
            # steps = 20
            # forward1(int(delay) / 1000.0, int(steps))
        else:
            print('Water present')
            # GPIO.output(LED_SOIL_PIN, False)
            data_soil = GPIO.input(SOIL_PIN)
            payload_data["soil"] = data_soil
            print(f"data_soil 2 : {data_soil}")

            # readSensorData2()
            # payload3 = str(data_soil)
            # print(payload3)
            # publish.single(MQTT_PATH, payload3, hostname=MQTT_SERVER)
            # delay = 50
            # steps = 200
            # backwards1(int(delay) / 1000.0, int(steps))

    soilm = GPIO.input(SOIL_PIN)
    time.sleep(2.0)

    return payload_data


def sensorMQTTDataSend():
    print("MQTT Sensor Data send thread started....... :)")
    while True:
        payload_data = {}
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        payload_data["time"] = dt_string

        payload_dht = dht_11()
        if payload_dht is not None:
            if 'temperature' in payload_dht:
                payload_data["temperature"] = payload_dht['temperature']
            if 'humidity' in payload_dht:
                payload_data["humidity"] = payload_dht['humidity']

        payload_ldr = ldr()
        if payload_ldr is not None:
            if 'light' in payload_ldr:
                payload_data["light"] = payload_ldr['light']

        payload_soil = soil()
        if payload_soil is not None:
            if 'soil' in payload_soil:
                payload_data["soil"] = payload_soil['soil']

        mqtt_payload = str(payload_data)
        print(mqtt_payload)
        publish.single(SENSOR_TOPIC, mqtt_payload, hostname=MQTT_SERVER)


# ---------------------------------------------------------------
def on_message(client, userdata, message):
    global writer
    action = str(message.payload.decode("utf-8"))
    print("Received msg is ", action)
    # payload_data = json.loads(s)
    payload_pddl = ast.literal_eval(action)
    light_output = None
    temp_output = None
    soil_output = None

    if 'light_action' in payload_pddl and payload_pddl['light_action'] is not None:
        light_output = payload_pddl['light_action']
    if 'temp_action' in payload_pddl and payload_pddl['temp_action'] is not None:
        temp_output = payload_pddl['temp_action']
    if 'soil_action' in payload_pddl and payload_pddl['soil_action'] is not None:
        soil_output = payload_pddl['soil_action']

    light_actuation(light_output)
    cooler_actuation(temp_output)
    pump_actuation(soil_output)


def light_actuation(light_output):
    LED_PIN = 18
    GPIO.setup(LED_PIN, GPIO.OUT)
    if light_output is not None:
        if light_output == 'switchonlight':
            print("LIGHTS: ON")
            GPIO.output(LED_PIN, True)
        else:
            print("LIGHTS: OFF")
            GPIO.output(LED_PIN, False)


def cooler_actuation(temp_output):
    if temp_output is not None:
        if temp_output == 'switchoncooler':
            print("COOLER: ON")
            delay = 50
            steps = 20
            forward(int(delay) / 1000.0, int(steps))
        elif temp_output == 'switchoffcooler':
            print("COOLER: OFF")
            delay = 50
            steps = 20
            backwards(int(delay) / 1000.0, int(steps))


def pump_actuation(soil_output):
    LED_SOIL_PIN = 3
    GPIO.setup(LED_SOIL_PIN, GPIO.OUT)

    if soil_output is not None:
        if soil_output == 'switchonvalve':
            print("PUMP: ON")
            GPIO.output(LED_SOIL_PIN, True)
            delay = 50
            steps = 20
            forward1(int(delay) / 1000.0, int(steps))
        elif soil_output == 'switchoffvalve':
            print("PUMP: OFF")
            GPIO.output(LED_SOIL_PIN, False)
            delay = 50
            steps = 200
            backwards1(int(delay) / 1000.0, int(steps))


pddl_mqtt_client = paho.Client("PDDL")  # create client object
pddl_mqtt_client.on_message = on_message

print("connecting to broker host", MQTT_SERVER)
pddl_mqtt_client.connect(MQTT_SERVER)  # connection establishment with broker


def pddlMQTTDataReceive():
    print("MQTT PDDL Data receive thread started....... :)")
    pddl_mqtt_client.subscribe(PDDL_TOPIC)  # subscribe topic test
    pddl_mqtt_client.loop_forever()


# ---------------------------------------------------------------


# -------------------------------------------------

t1 = threading.Thread(target=sensorMQTTDataSend)
t2 = threading.Thread(target=pddlMQTTDataReceive)
t1.start()
t2.start()
# ---------------------------------------------
