import json
import shutil
from .base import HomeServerApp
from .base import TEMPLATES


class Jackett(HomeServerApp):
    def setup(self):
        self.container.stop()
        self.setup_nginx()
        self.compose.start()
        self.copy_indexers()

    def copy_indexers(self):
        indexers_path = (self.path / 'Jackett' / 'Indexers')
        indexers_path.mkdir(parents=True, exists_ok=True)
        shutil.copytree((TEMPLATES / 'jackett').absolute(), indexers_path)

    def setup_nginx(self):
        config = self.path / 'Jackett' / 'ServerConfig.json'
        result = json.load(config.open('r'))
        result['BasePathOverride'] = '/trackers'
        json.dump(result, config.open('w'))
