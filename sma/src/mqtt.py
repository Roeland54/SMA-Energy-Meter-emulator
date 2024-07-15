import json
import logging
import time
import os
import paho.mqtt.client as mqtt
import util
from config import settings
from emeter import emeterPacket

def setup_mqtt(userdata):
    if settings["enable_mqtt"] is False:
        return None
    
    set_mqtt_settings()
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata = userdata, protocol=mqtt.MQTTv5)

    if settings["mqtt"]["username"] and settings["mqtt"]["password"]:
        mqtt_client.username_pw_set(settings["mqtt"]["username"], settings["mqtt"]["password"])
    port = 1883
    if util.keys_exists(settings["mqtt"], "port"):
        conf_port = settings["mqtt"]["port"]
        if isinstance(conf_port, int):
            if conf_port > 0:
                port = settings["mqtt"]["port"]

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(settings["mqtt"]["broker"], port)
    logging.info("Starting MQTT loop")
    mqtt_client.loop_start()
    return mqtt_client._thread

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logging.info("Connected to MQTT broker")
        client.subscribe("sma/emeter/+/state")
    else:
        logging.error(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    logging.info(f"Received message on topic {msg.topic}")
    serial_number = msg.topic.split('/')[2]
    data = json.loads(msg.payload)
    logging.debug(f"Message data: {data}")

    packet = emeterPacket(int(serial_number))
    packet.begin(int(time.time() * 1000))

    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER, round(data['powerIn'] * 10))
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER, round(data['powerOut'] *10))
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER, 0)
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER, 0)

    packet.addCounterValue(emeterPacket.SMA_POSITIVE_ENERGY, round(data['energyIn'] * 1000 * 3600))
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_ENERGY, round(data['energyOut'] * 1000 * 3600))

    packet.end()

    packet_data = packet.getData()[:packet.getLength()]
    destination_addresses = data.get('destinationAddresses', [])

    with userdata['lock']:
        userdata['packets'][serial_number] = (packet_data, destination_addresses)
        logging.info(f"Updated packet for serial number {serial_number}")

def set_mqtt_settings():
    if os.environ.get("IS_HA_ADDON"):
        if settings["mqtt"]["broker"] != "auto_broker" \
                or settings["mqtt"]["port"] != "auto_port" \
                or settings["mqtt"]["username"] != "auto_user" \
                or settings["mqtt"]["password"] != "auto_password":
            # If settings were manually set, use the manually set settings
            return None

        broker_host = os.getenv("MQTTHOST", None)
        broker_port = os.getenv("MQTTPORT", None)
        broker_user = os.getenv("MQTTUSER", None)
        broker_pass = os.getenv("MQTTPASS", None)

        if not broker_host or not broker_port:
            raise Exception("MQTT connection could not be established. Please check if your MQTT Add-On is running!")

        logging.debug("MQTT Credentials - Host " + broker_host + " Port: " + str(broker_port) +
                      " User: " + str(broker_user) + " Pass: " + str(broker_pass))

        settings["mqtt"]["broker"] = broker_host
        settings["mqtt"]["port"] = broker_port
        settings["mqtt"]["username"] = broker_user
        settings["mqtt"]["password"] = broker_pass