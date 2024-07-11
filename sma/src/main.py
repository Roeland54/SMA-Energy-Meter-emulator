import json
import time
import threading
import socket
import logging
import util
import paho.mqtt.client as mqtt
from config import settings
from emeter import emeterPacket

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

    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER, data['powerIn'])
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER, data['powerOut'])
    packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER, 0)
    packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER, 0)

    packet.addCounterValue(emeterPacket.SMA_POSITIVE_ENERGY, data['energyIn'])
    packet.addCounterValue(emeterPacket.SMA_NEGATIVE_ENERGY, data['energyOut'])

    packet.end()

    packet_data = packet.getData()[:packet.getLength()]
    destination_addresses = data.get('destinationAddresses', [])

    with userdata['lock']:
        userdata['packets'][serial_number] = (packet_data, destination_addresses)
        logging.info(f"Updated packet for serial number {serial_number}")


def udp_sender(userdata):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        with userdata['lock']:
            for serial_number, (packet_data, destination_addresses) in userdata['packets'].items():
                if destination_addresses:
                    for address in destination_addresses:
                        udp_socket.sendto(packet_data, (address, userdata['udp_port']))
                        logging.debug(f"Sent packet to {address} for serial number {serial_number}")
                else:
                    udp_socket.sendto(packet_data, (userdata['udp_address'], userdata['udp_port']))
                    logging.debug(f"Sent multicast packet for serial number {serial_number} packet data: {packet_data}")
        time.sleep(1)


def main():
    util.setup_logging()
    util.set_mqtt_settings()

    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, userdata={
        'packets': {},
        'lock': threading.Lock(),
        'udp_address': '239.12.255.254',
        'udp_port': 9522
    }, protocol=mqtt.MQTTv5)

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

    udp_thread = threading.Thread(target=udp_sender, args=(mqtt_client._userdata,))
    udp_thread.daemon = True
    udp_thread.start()

    logging.info("Starting MQTT loop")
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()