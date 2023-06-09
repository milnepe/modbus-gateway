#!/usr/bin/env python3

"""
Secure MQTT client for MODBUS RTU comms with RS Pro Logic Module (PN 917-6370)

For the RS Pro Logic Module there are 4 coils Q1, Q2, Q3,& Q4
these have decimal addreses 0, 1, 2, 3

To turn on contacts Q2 & Q3 publish the following message to the broker -
the PLC must be in idle mode:
$ clientuitto_pub -h rock-4se -t "test/plc1/coils_on" -m '{"coils":[1,2]}'

The RS Pro Logic Module has serveral registers that can be read/written - see documentation
in the Logic Module software for details.

A sample LD program is provided in ld - Run this on the Pro Logic sending the following
messages to modify the T1 timer registers and then reset them:

$ mosquitto_pub -h rock-4se -t "test/plc1/timer_set" -m '{"start_address": 0, "values":[20,0,0,10]}'
$ mosquitto_pub -h rock-4se -t "test/plc1/timer_set" -m '{"start_address": 4, "values":[20,0,0,10]}'
$ mosquitto_pub -h rock-4se -t "test/plc1/timer_set" -m '{"start_address": 8, "values":[20,0,0,10]}'
$ mosquitto_pub -h rock-4se -t "test/plc1/timer_set" -m '{"start_address": 12, "values":[20,0,0,10]}'
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

instrument1 = minimalmodbus.Instrument(PORT, ADDRESS)
instrument1.serial.baudrate = BAUDRATE

plc1 = Plcs(instrument1, num_coils=4)
plcs = {'plc1': plc1}  # Dict of plc instances
print(f"Connected to Plc: {instrument1.address} port: {instrument1.serial.port}")

invoker = Invoker()


def plc_lookup(topic: str) -> Plcs:
    """Return PLC in sub-topic"""
    sub_topic = topic.split('/')
    try:
        return plcs[sub_topic[1]]
    except KeyError:
        return None


def plc_coils_on(mosq, obj, msg):
    """Callback mapping TOPIC_ROOT/plc{n}/coils_on topic to CoilsOnCmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(CoilsOnCmd(plc_lookup(msg.topic), payload['coils']))
    logging.info("Coils on: %s, %s", msg.topic, msg.payload.decode('utf-8'))


def plc_coils_off(mosq, obj, msg):
    """Callback mapping TOPIC_ROOT/plc{n}/coils_off topic to CoilsOffCmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(CoilsOffCmd(plc_lookup(msg.topic), payload['coils']))
    logging.info("Coils off: %s, %s", msg.topic, msg.payload.decode('utf-8'))


def plc_timer_set(mosq, obj, msg):
    """Callback mapping TOPIC_ROOT/plc{n}/timer_set topic to TimerSetCmd"""
    payload = json.loads(msg.payload)
    invoker.set_command(TimerSetCmd(plc_lookup(msg.topic), payload['start_address'], payload['values']))
    logging.info("Timer set: %s, %s", msg.topic, msg.payload.decode('utf-8'))


def plc_timer_reset(mosq, obj, msg):
    """Callback mapping TOPIC_ROOT/plc{n}/timer_reset topic to ResetTimersCmd"""
    invoker.set_command(ResetTimersCmd(plc_lookup(msg.topic)))
    logging.info("Timer reset: %s, %s", msg.topic, msg.payload.decode('utf-8'))


def on_message(mosq, obj, msg):
    """Callback mapping all other TOPIC_ROOT messages - no ops"""
    logging.info("Unexpected message: %s, %s", msg.topic, msg.payload.decode('utf-8'))


def main() -> None:

    mqttc = mqtt.Client(CLIENT_ID)
    mqttc.tls_set(
        ca_certs=ROOT_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY
    )

    # Add specific message callbacks eg test/plc1/coils_on
    mqttc.message_callback_add(TOPIC_ROOT + "/+/coils_on", plc_coils_on)
    mqttc.message_callback_add(TOPIC_ROOT + "/+/coils_off", plc_coils_off)
    mqttc.message_callback_add(TOPIC_ROOT + "/+/timer_set", plc_timer_set)
    mqttc.message_callback_add(TOPIC_ROOT + "/+/timer_reset", plc_timer_reset)
    mqttc.on_message = on_message
    mqttc.connect(BROKER, 8883, 60)
    mqttc.subscribe(TOPIC_ROOT + "/#", 0)

    mqttc.loop_start()

    while True:
        invoker.invoke()


if __name__ == "__main__":
    main()
