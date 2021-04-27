from .base import HomeServerApp
import time
import yaml

PORTS = {
    "facebook": 29319,
    "instagram": 29330,
    "signal": 29328,
    "telegram": 29317,
    "whatsapp": 29318,
}


class Matrix(HomeServerApp):
    def setup_first_step(self):
        cfile = self.path / 'synapse' / 'homeserver.yaml'

        while not cfile.exists():
            time.sleep(1)

        config = yaml.load(cfile.open())
        config['server_name'] = f'matrix.{self.domain}'
        config['app_service_config_files'] = [
            # '/data/signal/registration.yaml',
            '/data/whatsapp/registration.yaml',
            # '/data/telegram/registration.yaml',
            # '/data/facebook/registration.yaml',
            # '/data/instagram/registration.yaml'
        ]
        yaml.dump(config, cfile.open('w'))
        services = ('whatsapp', 'facebook', 'instagram', 'signal', 'telegram')

        for service in services:
            hcfile = self.path / f'mautrix-{service}' / 'config.yaml'
            while not hcfile.exists():
                time.sleep(1)
            h_cfg = yaml.load(hcfile.open())

            addr = f'http://mautrix{service}:{PORTS[service]}'

            h_cfg['homeserver']['address'] = f'https://matrix.{self.domain}'
            h_cfg['homeserver']['domain'] = f'matrix.{self.domain}'
            h_cfg['appservice']['address'] = f'matrix.{self.domain}'
            h_cfg['appservice']['address'] = addr
            h_cfg['appservice']['hostname'] = 'mautrix{service}'
            if service == 'signal':
                h_cfg['database'] = 'postgres://pguser:pgpw@postgres/pguser'
            yaml.dump(h_cfg, hcfile.open('w'))
