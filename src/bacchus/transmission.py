import json
from .base import HomeServerApp


class Transmission(HomeServerApp):
    def setup_first_step(self):
        cfile = self.path / 'config' / 'settings.json'
        cfg = json.load(cfile.open())
        cfg['rpc-whitelist-enabled'] = False
        json.dump(cfg, cfile.open('w'))
