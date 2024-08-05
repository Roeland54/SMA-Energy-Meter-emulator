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

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if "debug_logging" in config.settings:
        if config.settings.get("debug_logging", False):
            logger.setLevel(logging.DEBUG)

    if "disable_logging" in config.settings:
        if config.settings.get("disable_logging", False):
            logger.setLevel(logging.ERROR)
