import json
import logging
import time
from contextlib import suppress
from lxml import etree
from .base import HomeServerApp
import requests

logging.basicConfig(level=logging.DEBUG)

PORTS = {'radarr': 7878, 'lidarr': 8686, 'sonarr': 8989}
TR_CFG = {
    "enable":
    True,
    "protocol":
    "torrent",
    "priority":
    1,
    "name":
    "transmission",
    "fields": [{
        "name": "host",
        "value": "transmission"
    }, {
        "name": "port",
        "value": 9091
    }, {
        "name": "urlBase",
        "value": "/transmission/"
    }, {
        "name": "username"
    }, {
        "name": "password"
    }, {
        "name": "tvCategory"
    }, {
        "name": "tvDirectory"
    }, {
        "name": "recentTvPriority",
        "value": 0
    }, {
        "name": "olderTvPriority",
        "value": 0
    }, {
        "name": "addPaused",
        "value": False
    }, {
        "name": "useSsl",
        "value": False
    }],
    "implementationName":
    "Transmission",
    "implementation":
    "Transmission",
    "configContract":
    "TransmissionSettings",
    "infoLink":
    "https://wiki.servarr.com/Sonarr_Supported_DownloadClients",
    "tags": []
}


def send(arr_name, api, arr_api_key, provider):
    """Send a query against arr api."""
    url = f'http://{arr_name}:{PORTS[arr_name]}/api/v3/{api}'
    headers = {'X-Api-Key': arr_api_key}
    logging.debug(requests.post(url, headers=headers, json=provider).text)


class Arr(HomeServerApp):
    def setup_first_step(self):
        cfg = (self.path / '..' / 'jackett' / 'Jackett' / 'ServerConfig.json')
        while not cfg.exists():
            logging.info(f"Waiting for {cfg}")
            time.sleep(1)
        japi_key = json.loads(cfg.read_text())['APIKey']
        keys = {}
        for arr in ('radarr', 'lidarr', 'sonarr'):
            cfile = (self.path / '..' / arr / 'config.xml')
            cfg = etree.fromstring(cfile.read_text())
            while not cfile.exists():
                logging.info(f"Waiting for {cfile}")
                time.sleep(1)
            cfg.find('UrlBase').text = f'/{arr}'
            logging.info(etree.tostring(cfg))
            (self.path / '..' / arr / 'config.xml').write_bytes(
                etree.tostring(cfg))
            keys[arr] = cfg.find('ApiKey').text
            with suppress(Exception):
                send(arr, 'downloadclient', keys[arr], TR_CFG)
        (self.path / '..' / '.env_jackett_sync').write_text(f"""
APIKEY={japi_key}
URL=http://jackett:9117
SONARR_URL=http://sonarr:8989
SONARR_KEY={keys['sonarr']}
RADARR_URL=http://radarr:7878
RADARR_KEY={keys['radarr']}
LIDARR_URL=http://lidarr:8686
LIDARR_KEY={keys['lidarr']}
""")
