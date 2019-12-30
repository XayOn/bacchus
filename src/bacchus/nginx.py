from .base import HomeServerApp
from .base import TEMPLATES
from pathlib import Path


class Nginx:
    def __init__(self, path, domain):
        self.path = Path(path)
        self.domain = domain

    def setup_certificates(self):
        """Setup certificates"""
        data_path = self.path / self.domain
        if not data_path.exists():
            data_path.mkdir(parents=True, exist_ok=True)
            # TODO: call docker API.
            self.docker.containers.run('frapsoft/openssl', detach=True)
            subprocess.check_output(
                f"docker run -v\"{data_path.parent.absolute()}:/etc/certs\" "
                f"frapsoft/openssl req -x509 -nodes -newkey rsa:4096 "
                f"-days 365 -keyout "
                f"'/etc/certs/{self.domain}/privkey.pem' -out "
                f"'/etc/certs/{self.domain}/fullchain.pem' "
                f"-subj '/CN={self.domain}'",
                shell=True)

    def setup_config(self):
        """Write nginx config.

        TODO: Use a proper templating system?
        """
        (self.path / 'nginx.conf').write_text(
            (TEMPLATES / 'nginx.tpl').read_text().format(domain=self.domain))

    def setup(self):
        self.setup_certificates()
        self.setup_config()
