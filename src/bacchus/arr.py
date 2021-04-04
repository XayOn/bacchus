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


def get_maincfg(name):
    port = PORTS[name]
    return {
        "bindAddress": "*",
        "port": port,
        "sslPort": port + 2020,
        "enableSsl": False,
        "launchBrowser": True,
        "authenticationMethod": "none",
        "analyticsEnabled": False,
        "logLevel": "info",
        "consoleLogLevel": "",
        "branch": "master",
        "apiKey": "e7e42d0aec804c36bde3072eb3f8d477",
        "sslCertPath": "",
        "sslCertPassword": "",
        "urlBase": f"/{name}",
        "updateAutomatically": False,
        "updateMechanism": "docker",
        "updateScriptPath": "",
        "proxyEnabled": False,
        "proxyType": "http",
        "proxyHostname": "",
        "proxyPort": 8080,
        "proxyUsername": "",
        "proxyPassword": "",
        "proxyBypassFilter": "",
        "proxyBypassLocalAddresses": True,
        "certificateValidation": "disabled",
        "backupFolder": "Backups",
        "backupInterval": 7,
        "backupRetention": 28,
        "id": 1
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


def send(arr_name, api, arr_api_key, provider):
    """Send a query against arr api."""
    url = f'http://{arr_name}:{PORTS[arr_name]}/api/v3/{api}'
    headers = {'X-Api-Key': arr_api_key}
    return requests.post(url, headers=headers, json=provider).text


class Arr(HomeServerApp):
    @property
    def setup_first_step(self):
        name = self.__class__.__name__.lower()
        cfg = (self.path / '..' / 'jackett' / 'Jackett' / 'ServerConfig.json')
        japi_key = json.loads(cfg.read_text())['APIKey']
        cfg = etree.fromstring((self.path / 'config.xml').read_text())
        api_key = cfg.find('ApiKey').text
        indexer_files = (TEMPLATES / 'jackett' / 'Indexers').glob('*.json')

        print(f"Configuring indexers on {self.__class__.__name__}")

        for name in (a.stem.lower() for a in indexer_files):
            print(f"Configuring {name} on {self.__class__.__name__}")
            # Setup each indexer
            with suppress(Exception):
                jurl = (f'http://jackett:9117/api/v3'
                        f'/indexers/{name}/results/torznab/')
                provider = get_provider(jurl, japi_key, name)
                send(name, 'indexer', api_key, provider)
        # Configure transmission
        send(name, 'downloadclient', api_key, TR_CFG)

        # Configure base path
        send(name, 'general', api_key, get_maincfg(self.name))


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
