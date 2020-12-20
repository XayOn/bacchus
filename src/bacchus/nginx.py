from .base import HomeServerApp
from .base import TEMPLATES
from pathlib import Path
from jinja2 import Template
import subprocess


class Nginx(HomeServerApp):
    def setup(self):
        self.logger.debug('Setting nginx configuration template')
        template = Template((TEMPLATES / 'nginx.tpl').read_text())

        services = {
            'Lidarr': ["lidarr", "8686"],
            'Radarr': ["radarr", "7878"],
            'Readarr': ["readarr", "8787"],
            'Sonarr': ["sonarr", "8989"],
            'Bazarr': ["bazarr", "6767"],

            'NextCloud': ["nextcloud", "80"],

            'Jackett': ["jackett", "9117"],
            'Transmission': ["transmission", "9091"],
            'PiHole': ['pihole', '80']

            'Jellyfin': ["jellyfin", "8096"],
            'Ubooquity': ["ubooquity", "2202"],
            'Homer': ["homer", "8080"],
            'Kodi': ['kodi', '8080'],

        }

        context = dict(domain=self.domain,
                       services=dict([
                           v for k, v in services.items()
                           if k in self.parent.selected_providers
                       ]),
                       selected=self.parent.selected_providers)

        (self.path / 'nginx.conf').write_text(template.render(**context))
