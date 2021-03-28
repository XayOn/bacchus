import xml.etree.ElementTree as ET
from .base import HomeServerApp


class Jellyfin(HomeServerApp):
    """Jellyfin"""

    def setup_first_step(self):
        config = ET.parse(str(self.path / 'system.xml'))
        config.find('BaseUrl').text = '/jellyfin/'
        config.write(str(self.config_file))
