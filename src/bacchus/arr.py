import json

from functools import cached_property
from .base import TEMPLATES, HomeServerApp

import requests
import xml.etree.ElementTree as ET

PORTS = {'radarr': 7878, 'lidarr': 8686, 'sonarr': 8989}


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


def send(arr_name, arr_api_key, jackett_api_key, provider):
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
    url = f'http://{arr_name}:{PORTS[arr_name]}/api/v3/indexer'
    jurl = f"http://jackett:9117/api/v2.0/indexers/{provider}/results/torznab/"
    headers = {'X-Api-Key': arr_api_key}
    provider = get_provider(jurl, jackett_api_key, provider)
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
            send(self.name, self.config.find('ApiKey').text, api_key, name)


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
