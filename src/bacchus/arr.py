import json
from lxml import etree
from contextlib import suppress

from .base import TEMPLATES, HomeServerApp

import requests

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


def get_provider(api_key, name):
    return {
        "enableRss":
        True,
        "enableAutomaticSearch":
        True,
        "enableInteractiveSearch":
        True,
        "supportsRss":
        True,
        "supportsSearch":
        True,
        "protocol":
        "torrent",
        "priority":
        25,
        "name":
        name,
        "fields": [{
            "name":
            "baseUrl",
            "value":
            f"http://jackett:9117/api/v2.0/indexers/{name}/results/torznab/"
        }, {
            "name": "apiPath",
            "value": "/api"
        }, {
            "name": "multiLanguages",
            "value": []
        }, {
            "name": "apiKey",
            "value": api_key
        }, {
            "name":
            "categories",
            "value": [2000, 2010, 2020, 2030, 2035, 2040, 2045, 2050, 2060]
        }, {
            "name": "additionalParameters"
        }, {
            "name": "removeYear",
            "value": False
        }, {
            "name": "minimumSeeders",
            "value": 1
        }, {
            "name": "seedCriteria.seedRatio"
        }, {
            "name": "seedCriteria.seedTime"
        }, {
            "name": "requiredFlags",
            "value": []
        }],
        "implementationName":
        "Torznab",
        "implementation":
        "Torznab",
        "configContract":
        "TorznabSettings",
        "infoLink":
        "https://wiki.servarr.com/Radarr_Supported_torznab",
        "tags": []
    }


def send(arr_name, api, arr_api_key, provider):
    """Send a query against arr api."""
    url = f'http://{arr_name}:{PORTS[arr_name]}/api/v3/{api}'
    headers = {'X-Api-Key': arr_api_key}
    print(requests.post(url, headers=headers, json=provider).text)


class Arr(HomeServerApp):
    def setup_first_step(self):
        name = self.__class__.__name__.lower()
        cfg = (self.path / '..' / 'jackett' / 'Jackett' / 'ServerConfig.json')
        japi_key = json.loads(cfg.read_text())['APIKey']
        cfg = etree.fromstring((self.path / 'config.xml').read_text())
        api_key = cfg.find('ApiKey').text
        indexer_files = (TEMPLATES / 'jackett' / 'Indexers').glob('*.json')

        print(f"Configuring indexers on {self.__class__.__name__}")

        for name_ in (a.stem.lower() for a in indexer_files):
            print(f"Configuring {name_} on {self.__class__.__name__}")
            # Setup each indexer
            with suppress(Exception):
                send(name, 'indexer', api_key, get_provider(japi_key, name_))
        # Configure transmission
        send(name, 'downloadclient', api_key, TR_CFG)
        cfg.find('UrlBase').text = f'/{name}'
        (self.path / 'config.xml').write_bytes(etree.tostring(cfg))


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
