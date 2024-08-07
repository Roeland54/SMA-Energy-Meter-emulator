import threading
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="CONF",
    settings_files=["settings.json", "/data/options.json", "settings.dev.json"],
)

workingdata = {
    'packets': {},
    'lock': threading.Lock(),
    'udp_address': '239.12.255.254',
    'udp_port': 9522,
    'homewizard_meters': {},
    'ip_serial_numbers': {}
}
