import logging
import os
import config

def keys_exists(element, *keys):
    """"
    Check if *keys (nested) exists in `element` (dict).
    Thanks stackoverflow: https://stackoverflow.com/questions/43491287/elegant-way-to-check-if-a-nested-key-exists-in-a-dict
    """
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

def set_mqtt_settings():
    if os.environ.get("IS_HA_ADDON"):
        if config.settings["mqtt"]["broker"] != "auto_broker" \
                or config.settings["mqtt"]["port"] != "auto_port" \
                or config.settings["mqtt"]["username"] != "auto_user" \
                or config.settings["mqtt"]["password"] != "auto_password":
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

        config.settings["mqtt"]["broker"] = broker_host
        config.settings["mqtt"]["port"] = broker_port
        config.settings["mqtt"]["username"] = broker_user
        config.settings["mqtt"]["password"] = broker_pass

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if "debug" in config.settings:
        if config.settings["debug"]:
            logger.setLevel(logging.DEBUG)

    if "disable_logging" in config.settings:
        if config.settings["disable_logging"]:
            logger.setLevel(logging.ERROR)
