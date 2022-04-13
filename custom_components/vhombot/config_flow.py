"""Config flow for lg-vhombot3."""
import my_pypi_dependency
import socket
import logging
import requests

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def find_devices():
    ip_address = get_ip()
    network_range = '.'.join(ip_address.split('.')[0:-1])
    print(network_range)
    devices = []
    for i in range(0, 255):
        try:
            r = requests.get("http://"+ network_range + str(i) + ":6260/status.txt", timeout=0.5)
            devices.append(network_range + str(i)) 
            _LOGGER.info(r.content)
            _LOGGER.info("Device found at: ", "192.168.1." + str(i))
        except:
            _LOGGER.debug("No Device found at: ", "192.168.1." + str(i))
    return devices


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    
    _LOGGER.info("Looking for vhombots!")
    devices = await hass.async_add_executor_job(find_devices())
    return len(devices) > 0


config_entry_flow.register_discovery_flow(DOMAIN, "lg-vhombot3", _async_has_devices)
