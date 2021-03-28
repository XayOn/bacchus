from functools import cached_property
import xml.etree.ElementTree as ET
from .base import HomeServerApp


class Jellyfin(HomeServerApp):
    """Jellyfin"""
    @property
    def config_file(self):
        return self.path / 'system.xml'

    @cached_property
    def config(self):
        return ET.parse(str(self.config_file))

    def setup_first_step(self):
        self.config.find('BaseUrl').text = '/jellyfin/'
        self.config.write(str(self.config_file))
