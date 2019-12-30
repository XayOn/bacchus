from functools import lru_cache
import xml.etree.ElementTree as ET

from .base import HomeServerApp


class Radarr(HomeServerApp):
    @property
    @lru_cache()
    def config(self):
        config_file = (self.path / 'data' / 'radarr' / 'config.xml').absolute()
        return ET.parse(str(config_file))

    def setup_nginx(self):
        self.config.find('UrlBase').text = '/movies/'
        self.config.write(str(self.config_file))

    def setup(self):
        self.setup_nginx()
