#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Send test messages over MQTT of type:
mosquitto_pub -t 'test/plc/coils_on' -m '{"coils":[1,2]}'
"""

import paho.mqtt.client as mqtt
import minimalmodbus
from invoker import Invoker
from plcs import Plcs
from commands import Coils_on_cmd, Coils_off_cmd, Validate_cmd 
from randomcoil import gen_coillist
import logging
import json

broker = "localhost"
rs485_port = "/dev/ttymxc3"
plc_address = 1
baudrate = 9600

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

rtu_dev = minimalmodbus.Instrument(rs485_port, plc_address)       
rtu_dev.serial.baudrate = baudrate = 9600

plc = Plcs(rtu_dev, num_coils=4)
print(f"Connected to Plc {rtu_dev.address} \
    on port: {rtu_dev.serial.port}")

invoker = Invoker()

def plc_coils_on(mosq, obj, msg):
    # Topic matching test/plc/coils_on
    payload = json.loads(msg.payload)
    invoker.set_command(Coils_on_cmd(plc, payload['coils']))
    invoker.invoke() 
    logging.info(f"Coils on: {msg.topic} {msg.payload.decode('utf-8')}")


def plc_coils_off(mosq, obj, msg):
    # Topic matching test/plc/coils_off
    payload = json.loads(msg.payload)
    invoker.set_command(Coils_off_cmd(plc, payload['coils']))
    invoker.invoke() 
    logging.info(f"Coils off: {msg.topic} {msg.payload.decode('utf-8')}")


def on_message(mosq, obj, msg):
    # Match other test messages
    logging.info(f"Coils on: {msg.topic} {msg.payload.decode('utf-8')}")


def main() -> None:

    client = mqtt.Client()

    # Add specific message callbacks
    client.message_callback_add("test/plc/coils_on", plc_coils_on)
    client.message_callback_add("test/plc/coils_off", plc_coils_off)
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.subscribe("test/#", 0)

    client.loop_forever()    

if __name__ == "__main__":
        main()
