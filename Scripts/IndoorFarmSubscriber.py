import csv
import os
import re
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time
import sys
import datetime
import time
import json
import ast

# ------------------------------- Declaration of host, topic names for publisher and subscriber ------------------------

broker = "192.168.0.101"  # host name
SENSOR_TOPIC = "indoor_farm"  # topic name
PDDL_TOPIC = "indoor_farm_pddl"

# ------------------------------  Creating a CSV file to log data  --------------------------------------------------

file = open("iotdata.csv", "w")
writer = csv.writer(file)
writer.writerow(["Time", "Temperature", "Humidity", "Light", "Light Energy", "Moisture", "Pump Energy"])


# file.close()

# --------------------------- Function for interpretation of plan files obtained after PDDL process -------------------

def parseFile(filename):
    f = open(filename, 'r+')
    lines = f.readlines()[0]
    f.close()

    lines = lines[1:]
    line_split = lines.split()
    action1 = line_split[0]
    print(action1)
    return action1

# ---------------------------- Function for running the AI planner based on domain and problem file -----------------

def run_planner(domainname, problem, out):
    myCmd = 'python Aiplanner.py {0} {1} {2}'
    myCmd = myCmd.format(domainname, problem, out)
    os.system(myCmd)
    action = parseFile(out)
    return action

# ---------------------------- Function for decoding and logging of sensor data --------------------------------------
def on_message(client, userdata, message):
    global writer
    s = str(message.payload.decode("utf-8"))
    print("Received msg is ", s)
    # payload_data = json.loads(s)
    payload_data = ast.literal_eval(s)
    excel_data = {'time': None, 'temperature': None, 'humidity': None, 'light': None, 'Light Energy': None, 'soil': None, 'Pump Energy': None}
    if 'time' in payload_data and payload_data['time'] is not None:
        excel_data['time'] = payload_data['time']
    if 'temperature' in payload_data and payload_data['temperature'] is not None:
        excel_data['temperature'] = payload_data['temperature']
    if 'humidity' in payload_data and payload_data['humidity'] is not None:
        excel_data['humidity'] = payload_data['humidity']
    if 'light' in payload_data and payload_data['light'] is not None:
        excel_data['light'] = payload_data['light']
    if 'Light Energy' in payload_data and payload_data['Light Energy'] is not None:
        excel_data['Light Energy'] = payload_data['Light Energy']
    if 'soil' in payload_data and payload_data['soil'] is not None:
        excel_data['soil'] = payload_data['soil']
    if 'Pump Energy' in payload_data and payload_data['Pump Energy'] is not None:
        excel_data['Pump Energy'] = payload_data['Pump Energy']

    print(f"Publisher data : {payload_data}")
    print(f"Excel data : {excel_data}")
    writer.writerow([excel_data['time'], excel_data['temperature'], excel_data['humidity'], excel_data['light'],
                     excel_data['Light Energy'], excel_data['soil'], excel_data['Pump Energy']])
# ------------------------------------------ Variables for actuation ------------------------------------------------

    light_action = None
    temp_action = None
    soil_action = None

# --------------------------------------- Assignments of domain and problem files -----------------------------------
    domain = 'Light_Domain.pddl'
    filename = 'lightplan.txt'
    if excel_data['light'] == 1:
        problem = 'Light_OnProb.pddl'
    else:
        problem = 'Light_OffProb.pddl'
    light_action = run_planner(domain, problem, filename)
    print(f"light_action : {light_action}")

    domainname= 'Temp_Domain.pddl'
    filename = 'tempplan.txt'
    if excel_data['temperature'] is not None:
        if excel_data['temperature'] > 26:
            problem = 'Temp_HighProb.pddl'
            temp_action = run_planner(domainname, problem, filename)
        elif excel_data['temperature'] < 22:
            problem = 'Temp_LowProb.pddl'
            temp_action = run_planner(domainname, problem, filename)
    print(f"temp_action : {temp_action}")
    domain = 'Moisture_Domain.pddl'
    filename = 'moistureplan.txt'
    if excel_data['soil'] == 0:
        problem = 'Moisture_HighProb.pddl'
    else:
        problem = 'Moisture_LowProb.pddl'
    soil_action = run_planner(domain, problem, filename)
    print(f"soil_action : {soil_action}")

    action = {}
    action['light_action'] = light_action
    action['temp_action'] = temp_action
    action['soil_action'] = soil_action

# --------------------------- MQTT code to publish data back to Raspberry Pi for actuation process -------------------
    mqtt_payload = str(action)
    print(mqtt_payload)
    publish.single(PDDL_TOPIC, mqtt_payload, hostname=broker)

    # file.close()

# ----------------------------- MQTT code to connect to host and topic for receiving sensor data----------------------
client = paho.Client("user")  # create client object
client.on_message = on_message

print("connecting to broker host", broker)
client.connect(broker)  # connection establishment with broker
print("subscribing begins here")
client.subscribe(SENSOR_TOPIC)  # subscribe topic test

while 1:
    client.loop_forever()  # continuously checking for message
