from contextlib import suppress
import json
import shutil
from .base import HomeServerApp
from .base import TEMPLATES


class Jackett(HomeServerApp):
    def setup(self):
        self.container.stop()
        config = self.path / 'Jackett' / 'ServerConfig.json'
        result = json.load(config.open('r'))
        result['BasePathOverride'] = '/jackett'
        json.dump(result, config.open('w'))
        self.copy_indexers()
        self.compose.start()

    def copy_indexers(self):
        indexers_path = (self.path / 'Jackett' / 'Indexers')
        with suppress(Exception):
            indexers_path.mkdir(parents=True)

        files = ((TEMPLATES / 'jackett' / 'Indexers').absolute()).glob('*')
        for file in files:
            shutil.copyfile(str(file.absolute()), indexers_path / file.name)
