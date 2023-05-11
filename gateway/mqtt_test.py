#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Send test messages over MQTT with json payload to control plc coils:
mosquitto_pub -t 'test/plc/coils_on' -m '{"coils":[1,2]}'
"""

import paho.mqtt.client as mqtt
import minimalmodbus
from invoker import Invoker
from plcs import Plcs
from commands import Coils_on_cmd, Coils_off_cmd
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

plc = Plcs(rtu_device, num_coils=4)
print(f"Connected to Plc: {rtu_device.address} port: {rtu_device.serial.port}")

invoker = Invoker()

def plc_coils_on(mosq, obj, msg):
    """Callback mapping topic_root/plc/coils_on topic to Coils_on_cmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(Coils_on_cmd(plc, payload['coils']))
    invoker.invoke() 
    logging.info(f"Coils on: {msg.topic} {msg.payload.decode('utf-8')}")


def plc_coils_off(mosq, obj, msg):
    """Callback mapping topic_root/plc/coils_off topic to Coils_off_cmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(Coils_off_cmd(plc, payload['coils']))
    invoker.invoke() 
    logging.info(f"Coils off: {msg.topic} {msg.payload.decode('utf-8')}")


def on_message(mosq, obj, msg):
    """Callback mapping all other topic_root messages - no ops"""
    logging.info(f"Coils on: {msg.topic} {msg.payload.decode('utf-8')}")


def main() -> None:

    client = mqtt.Client()

    # Add specific message callbacks
    client.message_callback_add(topic_root + "/plc/coils_on", plc_coils_on)
    client.message_callback_add(topic_root + "/plc/coils_off", plc_coils_off)
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.subscribe(topic_root + "/#", 0)

    client.loop_forever()    

if __name__ == "__main__":
        main()
