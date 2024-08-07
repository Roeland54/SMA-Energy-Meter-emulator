from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange
from config import settings, workingdata
import logging
import requests
import hashlib
from emeter import emeterPacket
import time
import json

def setup_homewizard():
    if settings.get("enable_homewizard", False) is False:
        return None
    
    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf, "_hwenergy._tcp.local.", handlers=[lambda zeroconf, service_type, name, state_change: on_service_state_change(zeroconf, service_type, name, state_change)])
    for ip in settings.get("homewizard_manual_addresses", []):
        ip = ip.lower()
        serial_number = string_to_int(ip)
        logging.info(f"HomeWizard manual entry ip/hostname: {ip}, assigned serial number: {serial_number}")
        workingdata['homewizard_meters'][ip] = serial_number

def on_service_state_change(zeroconf, service_type, name, state_change):
    if state_change is not ServiceStateChange.Added:
        return
    
    logging.debug(f"Found device with name: {name}, state_change: {state_change}, trying to get info")
    info = zeroconf.get_service_info(service_type, name)
    if not info:
        return
    hostname = info.server
    logging.debug(f"Found device with hostname from ServiceInfo: {hostname}")

    if not hostname.startswith("p1meter") and not hostname.startswith("kwhmeter"):
        return
    
    hostname = hostname.lower()
    if hostname in workingdata['homewizard_meters'].keys():
        return
    
    serial_number = string_to_int(hostname)
    
    logging.info(f"Found HomeWizard meter with hostname: {hostname}, assigned serial number: {serial_number}")
    with workingdata['lock']:
        workingdata['homewizard_meters'][hostname] = serial_number

def update_homewizard():
    if len(workingdata['homewizard_meters']) == 0:
        return None
    
    try:
        with workingdata['lock']:
            hostnames = workingdata['homewizard_meters']

        for (hostname, serial_number) in hostnames.items():
            packet = emeterPacket(int(serial_number))
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

            with workingdata['lock']:
                workingdata['packets'][serial_number] = (packet_data, destination_addresses)
                logging.debug(f"Updated homewizard packet for serial number {serial_number}")

    except requests.RequestException as e:
        logging.error(f"HTTP Request failed: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON payload: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    
def string_to_int(string_value):
    # Create a SHA-256 hash of the string
    hash_object = hashlib.sha256(string_value.encode())
    # Convert the hash to an integer
    hash_int = int(hash_object.hexdigest(), 16) % (10 ** 8)
    return hash_int