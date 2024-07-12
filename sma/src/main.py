import threading
import util
import mqtt
import udp

def main():
    util.setup_logging()
    util.set_mqtt_settings()

    userdata = {
        'packets': {},
        'lock': threading.Lock(),
        'udp_address': '239.12.255.254',
        'udp_port': 9522
    }

    mqtt.setup_mqtt(userdata)
    udp.setup_udp(userdata)

if __name__ == "__main__":
    main()