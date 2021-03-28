import json
from contextlib import suppress

from functools import cached_property
from .base import TEMPLATES, HomeServerApp

import requests
import xml.etree.ElementTree as ET

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


def get_provider(url, api_key, name):
    fields = [
        dict(name='baseUrl', value=url),
        dict(name="apiPath", value="/api"),
        dict(name="multiLanguages", value=[]),
        dict(name="apiKey", value=api_key),
        dict(name="categories",
             value=[2000, 2010, 2020, 2030, 2035, 2040, 2045, 2050, 2060]),
        dict(name="additionalParameters"),
        dict(name="removeYear", value=False),
        dict(name="minimumSeeders", value=1),
        dict(name="seedCriteria.seedRatio"),
        dict(name="seedCriteria.seedTime"),
        dict(name="requiredFlags", value=[]),
    ]
    return {
        "enableRss": True,
        "enableAutomaticSearch": True,
        "enableInteractiveSearch": True,
        "supportsRss": True,
        "supportsSearch": True,
        "protocol": "torrent",
        "priority": 25,
        "name": name,
        "fields": fields,
        "implementationName": "Torznab",
        "implementation": "Torznab",
        "configContract": "TorznabSettings",
        "infoLink": "https://wiki.servarr.com/Radarr_Supported_torznab",
        "tags": []
    }


def send(arr_name, api, arr_api_key, jackett_api_key, provider):
    """Create an indexer in an arr*

    assumes arrs are available at http://arr:arr_port/

    Arguments:

        arr_name: Arr name (radarr, lidarr, sonarr)
        arr_api_key: API key for the arr
        jackett_api_key: Jackett api key
        provider: Provider name (torrent site name)

    Usage:
        send("radarr", "f00asdf0123100", "1337x")
    """
    url = f'http://{arr_name}:{PORTS[arr_name]}/api/v3/{api}'
    headers = {'X-Api-Key': arr_api_key}
    return requests.post(url, headers=headers, json=provider).text


class Arr(HomeServerApp):
    @property
    def base_path(self):
        return f'/{self.name}'

    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def config_file(self):
        return self.path / 'config.xml'

    @cached_property
    def config(self):
        return ET.parse(str(self.config_file))

    def setup_first_step(self):
        self.config.find('UrlBase').text = self.base_path
        self.config.write(str(self.config_file))

    def setup_second_step(self):
        cfg = (self.path / '..' / 'jackett' / 'Jackett' / 'ServerConfig.json')
        api_key = json.loads(cfg.read_text())['APIKey']
        indexer_files = (TEMPLATES / 'jackett' / 'Indexers').glob('*.json')
        print(f"Configuring indexers on {self.__class__.__name__}")

        for name in (a.stem.lower() for a in indexer_files):
            print(f"Configuring {name} on {self.__class__.__name__}")
            with suppress(Exception):
                jurl = (f'http://jackett:9117/api/v3'
                        f'/indexers/{name}/results/torznab/')
                provider = get_provider(jurl, api_key, name)
                send(self.name, 'indexer',
                     self.config.find('ApiKey').text, provider)
        send(self.name, 'downloadclient', self.config.find('ApiKey'), TR_CFG)


class Lidarr(Arr):
    def settings(self, base_url, api_key):
        cats = [
            5010, 5030, 5040, 2000, 2010, 2020, 2030, 2035, 2040, 2045, 2050,
            2060
        ]
        return {
            "minimumSeeders": 1,
            "requiredFlags": [],
            "baseUrl": base_url,
            "multiLanguages": [],
            "apiKey": api_key,
            "categories": cats,
            "animeCategories": [],
            "removeYear": False,
            "searchByTitle": False,
        }


class Radarr(Arr):
    def settings(self, base_url, api_key):
        cats = [
            5010, 5030, 5040, 2000, 2010, 2020, 2030, 2035, 2040, 2045, 2050,
            2060
        ]
        return {
            "minimumSeeders": 1,
            "requiredFlags": [],
            "baseUrl": base_url,
            "multiLanguages": [],
            "apiKey": api_key,
            "categories": cats,
            "animeCategories": [],
            "removeYear": False,
            "searchByTitle": False,
        }


class Sonarr(Arr):
    def settings(self, base_url, api_key):
        cats = [
            5010, 5030, 5040, 2000, 2010, 2020, 2030, 2035, 2040, 2045, 2050,
            2060
        ]
        return {
            "minimumSeeders": 1,
            "requiredFlags": [],
            "baseUrl": base_url,
            "multiLanguages": [],
            "apiKey": api_key,
            "categories": cats,
            "animeCategories": [],
            "removeYear": False,
            "searchByTitle": False,
        }
