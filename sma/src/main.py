import util
import mqtt
import udp
import homewizard

def main():
    util.setup_logging()

    threads=[]

    mqtt_thread = mqtt.setup_mqtt()

    if mqtt_thread is not None:
        threads.append(mqtt_thread)

    homewizard.setup_homewizard()
    
    udp_thread = udp.setup_udp()

    if udp_thread is not None:
        threads.append(udp_thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
