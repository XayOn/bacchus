import json
from contextlib import suppress
from functools import lru_cache
from .base import TEMPLATES
import sqlite3
import xml.etree.ElementTree as ET

from .base import HomeServerApp


class Sonarr(HomeServerApp):
    @property
    def config_file(self):
        return self.path / 'config.xml'

    @property
    @lru_cache()
    def config(self):
        return ET.parse(str(self.config_file))

    def setup_nginx(self):
        self.config.find('UrlBase').text = '/subtitles/'
        self.config.write(str(self.config_file))

    def setup(self):
        self.setup_nginx()
        if self.container:
            self.container.stop()
        self.compose.start()
