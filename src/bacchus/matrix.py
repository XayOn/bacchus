from .base import HomeServerApp
import yaml


class Matrix(HomeServerApp):
    def setup_first_step(self):
        cfile = self.path / 'synapse' / 'homeserver.yaml'
        config = yaml.load(cfile.open())
        config['server_name'] = 'matrix.{self.domain}'
        config['app_service_config_files'] = [
            '/data/signal/registration.yaml',
            '/data/whatsapp/registration.yaml',
            '/data/telegram/registration.yaml',
            '/data/facebook/registration.yaml'
            '/data/instagram/registration.yaml'
        ]
        yaml.dump(config, cfile.open('w'))
        services = ('whatsapp', 'facebook', 'instagram', 'signal', 'telegram')

        for service in services:
            hcfile = self.path / f'mautrix-{service}' / 'config.yaml'
            h_cfg = yaml.load(hcfile.open())
            addr = 'http://mautrix{service}:{PORTS["service"]}'

            h_cfg['homeserver']['address'] = 'https://matrix.{self.domain}'
            h_cfg['homeserver']['domain'] = 'matrix.{self.domain}'
            h_cfg['appservice']['address'] = 'matrix.{self.domain}'
            h_cfg['appservice']['address'] = addr
            h_cfg['appservice']['hostname'] = 'mautrix{service}'
            yaml.dump(h_cfg, hcfile.open('w'))
