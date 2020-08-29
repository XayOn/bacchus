from .base import HomeServerApp
from .base import TEMPLATES
from pathlib import Path
import subprocess


class Nginx(HomeServerApp):
    def setup(self):
        self.logger.debug('Setting nginx configuration template')
        (self.path / 'nginx.conf').write_text(
            (TEMPLATES / 'nginx.tpl').read_text().format(domain=self.domain))
