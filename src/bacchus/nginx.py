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
            'Transmission': ["transmission", "9091"],
            'Lidarr': ["lidarr", "8686"],
            'Jellyfin': ["jellyfin", "8096"],
            'NextCloud': ["nextcloud", "80"],
            'Medusa': ["medusa", "8081"],
            'LazyLibrarian': ["lazylibrarian", "5299"],
            'Radarr': ["radarr", "7878"],
            'Jackett': ["jackett", "9117"],
            'Kodi': ['kodi', '8080'],
            'PiHole': ['pihole', '80']
        }

        context = dict(domain=self.domain,
                       services=dict([
                           v for k, v in services.items()
                           if k in self.parent.selected_providers
                       ]),
                       selected=self.parent.selected_providers)

        (self.path / 'nginx.conf').write_text(template.render(**context))
