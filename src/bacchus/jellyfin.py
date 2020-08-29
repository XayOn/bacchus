from functools import lru_cache
import xml.etree.ElementTree as ET
from .base import HomeServerApp


class Jellyfin(HomeServerApp):
    """Jellyfin"""
    @property
    def config_file(self):
        return self.path / 'system.xml'

    @property
    @lru_cache()
    def config(self):
        return ET.parse(str(self.config_file))

    def setup_nginx(self):
        self.config.find('BaseUrl').text = '/jellyfin/'
        self.config.write(str(self.config_file))

    def setup(self):
        self.setup_nginx()
