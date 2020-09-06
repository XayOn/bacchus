from .base import HomeServerApp
from .base import TEMPLATES
from pathlib import Path
from jinja2 import Template
import subprocess


class Nginx(HomeServerApp):
    def setup(self):
        self.logger.debug('Setting nginx configuration template')
        template = Template((TEMPLATES / 'nginx.tpl').read_text())
        context = dict(domain=self.domain, )
        (self.path / 'nginx.conf').write_text(template.render(**context))
