import json

from functools import lru_cache
from .base import TEMPLATES, HomeServerApp

import requests
import xml.etree.ElementTree as ET


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


def send(url, arr_name, arr_api_key, jackett_api_key, provider):
    """Create an indexer in an arr*

    Arguments:

        url: Base url containing both jackett and the arr*
        provider: Provider name (torrent site name)
        arr_name: Arr name (radarr, lidarr, sonarr)
        arr_api_key: API key for the arr

    Usage:
        send("https://private.foo.com/", "radarr", "f00asdf0123100", "1337x")
    """
    print(f'{url}{arr_name}/api/v3/indexer')
    return requests.post(
        f'{url}{arr_name}/api/v3/indexer',
        headers={
            'X-Api-Key': arr_api_key
        },
        json=get_provider(
            f"{url}jackett/api/v2.0/indexers/{provider}/results/torznab/",
            jackett_api_key, provider)).text


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

    @property
    @lru_cache()
    def config(self):
        return ET.parse(str(self.config_file))

    def setup_first_step(self):
        self.config.find('UrlBase').text = self.base_path
        self.config.write(str(self.config_file))

    def setup_second_step(self):
        api_key = json.loads((self.path / '..' / 'jackett' / 'Jackett' /
                              'ServerConfig.json').read_text())['APIKey']
        indexer_files = (TEMPLATES / 'jackett' / 'Indexers').glob('*.json')
        print(f"Configuring indexers on {self.__class__.__name__}")

        for name in (a.stem.lower() for a in indexer_files):
            print(f"Configuring {name} on {self.__class__.__name__}")
            print(
                send(f"https://private.{self.domain}/", self.name,
                     self.config.find('ApiKey').text, api_key, name))


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
