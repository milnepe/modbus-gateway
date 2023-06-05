#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MQTT client controlling plc coils via MODBUS RTU
Plc and command are mapped from topic
Json payload defines coil address to operate on

For the RS Pro Logic Module (PN 917-6370) there are 4 coils [0,1,2,3]
To turn on contacts Q2 & Q3 publish the following:
$ num=1
$ mosquitto_pub -t "test/plc$num/coils_on" -m '{"coils":[1,2]}'
"""

import paho.mqtt.client as mqtt
import minimalmodbus
from gateway.invoker import Invoker
from gateway.plcs import Plcs
from gateway.commands import CoilsOnCmd, CoilsOffCmd
import logging
import json

broker = "localhost"
rtu_port = "/dev/ttymxc3"
plc_address = 1
baudrate = 9600
topic_root = "test"

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

rtu_device = minimalmodbus.Instrument(rtu_port, plc_address)       
rtu_device.serial.baudrate = baudrate

plc1 = Plcs(rtu_device, num_coils=4)
print(f"Connected to Plc: {rtu_device.address} port: {rtu_device.serial.port}")

invoker = Invoker()

def plc_coils_on(mosq, obj, msg):
    """Callback mapping topic_root/plc1/coils_on topic to CoilsOnCmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(CoilsOnCmd(plc1, payload['coils']))
    invoker.invoke() 
    logging.info(f"Coils on: {msg.topic} {msg.payload.decode('utf-8')}")


def plc_coils_off(mosq, obj, msg):
    """Callback mapping topic_root/plc1/coils_off topic to CoilsOffCmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(CoilsOffCmd(plc1, payload['coils']))
    invoker.invoke() 
    logging.info(f"Coils off: {msg.topic} {msg.payload.decode('utf-8')}")


def on_message(mosq, obj, msg):
    """Callback mapping all other topic_root messages - no ops"""
    logging.info(f"Unexpected message: {msg.topic} {msg.payload.decode('utf-8')}")


def main() -> None:

    client = mqtt.Client()

    # Add specific message callbacks
    client.message_callback_add(topic_root + "/plc1/coils_on", plc_coils_on)
    client.message_callback_add(topic_root + "/plc1/coils_off", plc_coils_off)
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.subscribe(topic_root + "/#", 0)

    client.loop_forever()    

if __name__ == "__main__":
        main()
