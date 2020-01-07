from .base import HomeServerApp
from .base import TEMPLATES
from pathlib import Path
import subprocess


class Nginx(HomeServerApp):
    def setup_certificates(self):
        """Setup certificates"""
        data_path = self.path / self.domain
        data_path.mkdir(parents=True, exist_ok=True)
        local_path = '/etc/certs/'

        try:
            cmd = [
                "req", "-x509", "-nodes", "-newkey", "rsa:4096", "-days",
                "365", "-keyout", f"{local_path}{self.domain}/privkey.pem",
                "-out", f"{local_path}/{self.domain}/fullchain.pem", "-subj",
                f"/CN={self.domain}"
            ]
            self.logger.debug(f'executing {" ".join(cmd)}')
            result = self.client.containers.run('frapsoft/openssl',
                                                command=cmd,
                                                volumes={
                                                    self.path.absolute(): {
                                                        'bind': local_path,
                                                        'mode': 'rw'
                                                    }
                                                },
                                                auto_remove=True,
                                                detach=False)
            self.logger.debug(result)
        except Exception as err:
            self.logger.exception('could not create ssl certs')
        self.logger.debug(list(data_path.glob('*')))

    def setup_config(self):
        """Write nginx config."""
        (self.path / 'nginx.conf').write_text(
            (TEMPLATES / 'nginx.tpl').read_text().format(domain=self.domain))

    def setup(self):
        self.logger.debug("Setting up certificates")
        self.setup_certificates()
        self.logger.debug('Setting nginx configuration template')
        self.setup_config()
