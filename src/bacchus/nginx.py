from .base import HomeServerApp
from .base import TEMPLATES
from pathlib import Path
import subprocess


class Nginx(HomeServerApp):
    def setup_certificates(self):
        """Setup certificates"""
        data_path = self.path / self.domain
        data_path.mkdir(parents=True, exist_ok=True)
        self.docker.containers.run(
            'frapsoft/openssl',
            command=[
                "req", "-x509", "-nodes", "-newkey", "rsa:4096", "-days",
                "365", "-keyout", "/etc/certs/{self.domain}/privkey.pem",
                "-out", "/etc/certs/{self.domain}/fullchain.pem", "-subj",
                "/CN={self.domain}"
            ],
            volumes={data_path.parent.absolute(): '/etc/certs/'},
            auto_remove=True,
            detach=True)

    def setup_config(self):
        """Write nginx config.

        TODO: Use a proper templating system?
        """
        (self.path / 'nginx.conf').write_text(
            (TEMPLATES / 'nginx.tpl').read_text().format(domain=self.domain))

    def setup(self):
        self.setup_certificates()
        self.setup_config()
