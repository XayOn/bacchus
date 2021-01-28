import json
from .base import HomeServerApp


class Transmission(HomeServerApp):
    def setup_first_step(self):
        cfg = json.load((self.path / 'config' / 'settings.json').open())
        cfg['rpc-whitelist-enabled'] = False
        print(cfg)
        json.dump(cfg, (self.path / 'config' / 'settings.json').open('w'))
