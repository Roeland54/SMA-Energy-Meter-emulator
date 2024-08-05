import threading
import util
import mqtt
import udp
import homewizard

def main():
    util.setup_logging()

    userdata = {
        'packets': {},
        'lock': threading.Lock(),
        'udp_address': '239.12.255.254',
        'udp_port': 9522,
        'homewizard_meters': {}
    }

    threads=[]

    mqtt_thread = mqtt.setup_mqtt(userdata)

    homewizard.setup_homewizard(userdata)

    if mqtt_thread is not None:
     threads.append(mqtt_thread)

    udp_thread = udp.setup_udp(userdata)

    if udp_thread is not None:
       threads.append(udp_thread)

    for thread in threads:
     thread.join()

if __name__ == "__main__":
    main()