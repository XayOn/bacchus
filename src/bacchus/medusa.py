import configparser
from .base import HomeServerApp


class Medusa(HomeServerApp):
    @property
    def config_file(self):
        return self.path / 'config.ini'

    def setup_nginx(self):
        config = configparser.ConfigParser()
        config.read(str(self.config_file))
        config.set('General', 'web_root', '/tv')
        with open(self.config_file, 'w') as fileo:
            config.write(fileo)

    def setup(self):
        self.setup_nginx()