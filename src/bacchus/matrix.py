from .base import HomeServerApp
import yaml


class Matrix(HomeServerApp):
    def setup_first_step(self):
        config = self.path / 'synapse' / 'homeserver.yaml'
        config = yaml.load(open(str(config)))
        config['server_name'] = 'matrix.{self.domain}'
        config['app_service_config_files'] = [
            '/data/signal/registration.yaml',
            '/data/whatsapp/registration.yaml',
            '/data/telegram/registration.yaml',
            '/data/facebook/registration.yaml'
            '/data/instagram/registration.yaml'
        ]
        yaml.dump(config, (self.path / 'synapse' / 'homeserver.yaml').open())
        services = ('whatsapp', 'facebook', 'instagram', 'signal', 'telegram')

        for service in services:
            config = self.path / f'mautrix-{service}' / 'config.yaml'
            h_cfg = yaml.load(open(str(config)))
            h_cfg['homeserver']['address'] = 'https://matrix.{self.domain}'
            h_cfg['homeserver']['domain'] = 'matrix.{self.domain}'
            h_cfg['appservice']['address'] = 'matrix.{self.domain}'
            h_cfg['appservice'][
                'address'] = 'http://mautrix{service}:{PORTS["service"]}'
            h_cfg['appservice']['hostname'] = 'mautrix{service}'
            yaml.dump(h_cfg, (self.path / f'mautrix-{service}' / 'config.yaml').open())
