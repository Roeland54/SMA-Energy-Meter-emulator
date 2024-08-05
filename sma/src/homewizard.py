from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange
import socket
from config import settings
import logging
import requests
from emeter import emeterPacket
import time
import json
import random

def setup_homewizard(userdata):
    if settings.get("enable_homewizard", False) is False:
        return None
    
    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf, "_hwenergy._tcp.local.", handlers=[lambda zeroconf, service_type, name, state_change: on_service_state_change(zeroconf, service_type, name, state_change, userdata)])
    random.seed(42)
    for ip in settings.get("homewizard_manual_addresses", []):
        settings['ip_serial_numbers'][ip] = (ip, hash(ip))

def on_service_state_change(zeroconf, service_type, name, state_change, userdata):
    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            hostname = socket.inet_ntoa(info.address)
            if hostname.startswith("p1meter") or hostname.startswith("kwhmeter"):
                random.seed(42)
                serial_number = hash(hostname)
                logging.info(f"Found Homewizard meter with hostname: {hostname}, assigned serial number: {serial_number}")
                with userdata['lock']:
                    userdata['homewizard_meters'][hostname] = (hostname + ".local", serial_number)

def update_homewizard(userdata):
    if settings.get("enable_homewizard", False) is False or (len(userdata['homewizard_meters']) == 0 and len(settings.get("homewizard_manual_addresses", [])) == 0):
        return None
    
    try:
        with userdata['lock']:
            hostnames = userdata['homewizard_meters']

        for (hostname, serial_number) in hostnames.items() + settings.get("ip_serial_numbers", []).items():
            # Perform the GET request
            response = requests.get(f'http://{hostname}/api/v1/data')
            
            # Raise an exception for HTTP errors
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()
            logging.debug(f"Message data: {data}")

            # Create a packet instance
            packet = emeterPacket(int(serial_number))
            packet.begin(int(time.time() * 1000))

            # Extract values from the JSON data and add them to the packet
            # Process active power values
            active_power = data['active_power_w']
            if active_power > 0:
                packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER, round(active_power * 10))
                packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER, 0)
            else:
                packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_ACTIVE_POWER, 0)
                packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_ACTIVE_POWER, round(active_power * -10))  # Sending absolute value for negative

            packet.addMeasurementValue(emeterPacket.SMA_POSITIVE_REACTIVE_POWER, 0)
            packet.addMeasurementValue(emeterPacket.SMA_NEGATIVE_REACTIVE_POWER, 0)

            # Sum the total energy imports (t1 and t2)
            total_power_import_kwh = data['total_power_import_t1_kwh'] + data['total_power_import_t2_kwh']
            packet.addCounterValue(emeterPacket.SMA_POSITIVE_ENERGY, round(total_power_import_kwh * 1000 * 3600))

            # Sum the total energy exports (t1 and t2)
            total_power_export_kwh = data['total_power_export_t1_kwh'] + data['total_power_export_t2_kwh']
            packet.addCounterValue(emeterPacket.SMA_NEGATIVE_ENERGY, round(total_power_export_kwh * 1000 * 3600))

            packet.end()

            # Get packet data
            packet_data = packet.getData()[:packet.getLength()]
            destination_addresses = settings.get("homewizard_destination_addresses", [])

            with userdata['lock']:
                userdata['packets'][serial_number] = (packet_data, destination_addresses)
                logging.info(f"Updated homewizard packet for serial number {serial_number}")

    except requests.RequestException as e:
        logging.error(f"HTTP Request failed: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON payload: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    
