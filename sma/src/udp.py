import time
import socket
import logging
import threading
import homewizard

def setup_udp(userdata):
    udp_thread = threading.Thread(target=udp_sender, args=(userdata,))
    udp_thread.daemon = True
    udp_thread.start()
    return udp_thread

def udp_sender(userdata):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    logging.info('Starting udp loop')
    while True:
        homewizard.update_homewizard(userdata)

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
