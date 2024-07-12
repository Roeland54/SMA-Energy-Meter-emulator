import threading
import util
import mqtt
import udp

def main():
    util.setup_logging()

    userdata = {
        'packets': {},
        'lock': threading.Lock(),
        'udp_address': '239.12.255.254',
        'udp_port': 9522
    }

    threads=[]

    mqtt_thread = mqtt.setup_mqtt(userdata)

    if mqtt_thread is not None:
     threads.append(mqtt_thread)

    udp.setup_udp(userdata)

    for thread in threads:
     thread.join()

if __name__ == "__main__":
    main()