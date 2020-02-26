import json
from functools import lru_cache
from .base import TEMPLATES
import sqlite3
import xml.etree.ElementTree as ET

from .base import HomeServerApp


class Lidarr(HomeServerApp):
    @property
    def config_file(self):
        return self.path / 'config.xml'

    @property
    @lru_cache()
    def config(self):
        return ET.parse(str(self.config_file))

    def setup_nginx(self):
        self.config.find('UrlBase').text = '/music/'
        self.config.write(str(self.config_file))

    def setup_indexers(self):
        api_key = json.loads((self.path / '..' / 'jackett' / 'Jackett' /
                              'ServerConfig.json').read_text())['APIKey']
        indexer_files = (TEMPLATES / 'jackett' / 'Indexers').glob('*.json')
        indexers = []
        for num, name in enumerate((a.stem.lower() for a in indexer_files)):
            base_url = (f"https://private.{self.domain}/trackers/api/v2.0/"
                        f"indexers/{name}/results/torznab/")
            categories = [3000, 3010, 3020, 3030, 3040]
            settings = {
                "minimumSeeders": 1,
                "baseUrl": base_url,
                "apiKey": api_key,
                "apiPath": "/api",
                "seedCriteria": "{}",
                "categories": categories,
            }
            indexers.append([
                num + 1, name, 'Torznab',
                json.dumps(settings), 'TorznabSettings', 1, 1, 1
            ])

        conn = sqlite3.connect(str((self.path / 'nzbdrone.db').absolute()))
        cursor = conn.cursor()
        cursor.executemany('insert into Indexers values (?, ?, ?, ?, ?, ?, ?)',
                           indexers)
        conn.commit()
        conn.close()



    def setup(self):
        self.setup_nginx()
