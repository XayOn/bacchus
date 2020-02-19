import json
from .base import HomeServerApp


class Transmission(HomeServerApp):
    def setup(self):
        self.container.stop()
        set = json.load((self.path / 'config' / 'settings.json').read_bytes())
        set['rpc-whitelist-enabled'] = False
        (self.path / 'config' / 'settings.json').write_bytes(json.dumps(set))
