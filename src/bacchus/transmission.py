import json
from .base import HomeServerApp


class Transmission(HomeServerApp):
    def setup(self):
        if self.container:
            self.container.stop()
        cfg = json.loads((self.path / 'config' / 'settings.json').read_bytes())
        cfg['rpc-whitelist-enabled'] = False
        (self.path / 'config' / 'settings.json').write_text(json.dumps(cfg))
        self.compose.start()
