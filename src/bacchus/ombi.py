from bacchus.base import HomeServerApp
import requests


class Ombi(HomeServerApp):
    def setup_second_step(self):
        # TODO: Find out jellyfin API KEY...
        # Enable jellyfin
        server = {
            "ip": f"https://private.{self.domain}/jellyfin",
            "administratorId": "",
            "id": 0,
            "apiKey": '',
            "enableEpisodeSearching": False,
            "name": "Default",
            "port": "443",
            "ssl": True,
            "subDir": "",
            "serverHostname": ""
        }
        data = {
            "servers": [server],
            "isJellyfin": True,
            "id": 0,
            "enable": True
        }
        requests.post(f'https://private.{self.domain}/ombi/api/v1/Emby/',
                      json=data)

        # Enable sonarr
        api_key = self.providers['Sonarr'].config.find('ApiKey').text
        requests.post(
            f"https://private.{self.domain}/ombi/api/v1/Settings/Sonarr", {
                "enabled": True,
                "apiKey": api_key,
                "qualityProfile": "1",
                "rootPath": "1",
                "qualityProfileAnime": None,
                "rootPathAnime": None,
                "ssl": True,
                "subDir": "/radarr",
                "ip": self.domain,
                "port": "443",
                "addOnly": False,
                "seasonFolders": False,
                "v3": True,
                "languageProfile": 0
            })

        # Enable radarr
        api_key = self.providers['Radarr'].config.find('ApiKey').text
        requests.post(
            f"https://private.{self.domain}/ombi/api/v1/Settings/Radarr", {
                "enabled": True,
                "apiKey": api_key,
                "defaultQualityProfile": "1",
                "defaultRootPath": "/movies",
                "ssl": True,
                "subDir": "/radarr",
                "ip": "private.dionysos.tech",
                "port": "443",
                "addOnly": False,
                "minimumAvailability": "InCinemas"
            })
