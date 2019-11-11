import json
from .base import HomeServerApp


class Jackett(HomeServerApp):
    def setup(self):
        self.container.stop()
        self.setup_nginx()
        self.compose.start()

    def setup_nginx(self):
        config = self.path / 'Jackett' / 'ServerConfig.json'
        result = json.load(config.open('r'))
        result['BasePathOverride'] = '/trackers'
        json.dump(result, config.open('w'))
