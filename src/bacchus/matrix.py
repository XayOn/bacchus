from .base import HomeServerApp
import yaml


class Matrix(HomeServerApp):
    def setup_first_step(self):
        config = self.path / 'synapse' / 'homeserver.yaml'
        config = yaml.load(config)
        config['server_name'] = 'matrix.{self.domain}'
        config['app_service_config_files'] = [
            '/data/signal/registration.yaml',
            '/data/whatsapp/registration.yaml',
            '/data/telegram/registration.yaml',
            '/data/facebook/registration.yaml'
        ]
        yaml.dump(config, self.path / 'synapse' / 'homeserver.yaml')
