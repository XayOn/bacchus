import json
from .base import HomeServerApp


class Transmission(HomeServerApp):
    def setup_first_step(self):
        cfg = json.load((self.path / 'config' / 'settings.json').open())
        cfg['rpc-whitelist-enabled'] = False
        with open(cfg, 'w') as fileo:
            json.dump(cfg, fileo)
