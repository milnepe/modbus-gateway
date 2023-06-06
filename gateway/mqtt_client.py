#!/usr/bin/env python3

"""
MQTT client controlling plc coils via MODBUS RTU
Plc and command are mapped from topic
Json payload defines coil address to operate on

For the RS Pro Logic Module (PN 917-6370) there are 4 coils [0,1,2,3]
To turn on contacts Q2 & Q3 publish the following:
$ mosquitto_pub -h rock-4se -t "test/plc1/coils_on" -m '{"coils":[1,2]}'
$ mosquitto_pub -h rock-4se -t "test/plc1/timer_set" -m '{"start_address": 0, "values":[20,0,0,10]}'
$ mosquitto_pub -h rock-4se -t "test/plc1/timer_reset" -m ''
"""

import paho.mqtt.client as mqtt
import minimalmodbus
from gateway.invoker import Invoker
from gateway.plcs import Plcs
from gateway.commands import CoilsOnCmd, CoilsOffCmd, TimerSetCmd, ResetTimersCmd
import logging
import json

BROKER = 'rock-4se'
PORT = '/dev/ttymxc3'
ADDRESS = 1
BAUDRATE = 9600
CLIENT_ID = 'client01'
ROOT_CERT = 'certs/root_ca.crt'
CLIENT_CERT = 'certs/client01.crt'
CLIENT_KEY = 'certs/client01.key'
TOPIC_ROOT = "test"

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

rtu_device = minimalmodbus.Instrument(PORT, ADDRESS)       
rtu_device.serial.baudrate = BAUDRATE

plc1 = Plcs(rtu_device, num_coils=4)
print(f"Connected to Plc: {rtu_device.address} port: {rtu_device.serial.port}")

invoker = Invoker()

def plc_coils_on(mosq, obj, msg):
    """Callback mapping TOPIC_ROOT/plc1/coils_on topic to CoilsOnCmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(CoilsOnCmd(plc1, payload['coils']))
    invoker.invoke() 
    logging.info(f"Coils on: {msg.topic} {msg.payload.decode('utf-8')}")


def plc_coils_off(mosq, obj, msg):
    """Callback mapping TOPIC_ROOT/plc1/coils_off topic to CoilsOffCmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(CoilsOffCmd(plc1, payload['coils']))
    invoker.invoke() 
    logging.info(f"Coils off: {msg.topic} {msg.payload.decode('utf-8')}")

def plc_timer_set(mosq, obj, msg):
    """Callback mapping TOPIC_ROOT/plc1/timer_set topic to TimerSetCmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(TimerSetCmd(plc1, payload['start_address'], payload['values']))
    invoker.invoke() 
    logging.info(f"Timer set: {msg.topic} {msg.payload.decode('utf-8')}")

def plc_timer_reset(mosq, obj, msg):
    """Callback mapping TOPIC_ROOT/plc1/timer_reset topic to ResetTimersCmd"""
    invoker.set_command(ResetTimersCmd(plc1))
    invoker.invoke() 
    logging.info(f"Timer reset: {msg.topic} {msg.payload.decode('utf-8')}")

def on_message(mosq, obj, msg):
    """Callback mapping all other TOPIC_ROOT messages - no ops"""
    logging.info(f"Unexpected message: {msg.topic} {msg.payload.decode('utf-8')}")


def main() -> None:

    client = mqtt.Client(CLIENT_ID)
    client.tls_set(
        ca_certs=ROOT_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY
    )

    # Add specific message callbacks
    client.message_callback_add(TOPIC_ROOT + "/plc1/coils_on", plc_coils_on)
    client.message_callback_add(TOPIC_ROOT + "/plc1/coils_off", plc_coils_off)
    client.message_callback_add(TOPIC_ROOT + "/plc1/timer_set", plc_timer_set)
    client.message_callback_add(TOPIC_ROOT + "/plc1/timer_reset", plc_timer_reset)
    client.on_message = on_message
    client.connect(BROKER, 8883, 60)
    client.subscribe(TOPIC_ROOT + "/#", 0)

    client.loop_forever()    

if __name__ == "__main__":
        main()
