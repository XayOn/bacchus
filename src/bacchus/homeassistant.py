from .base import HomeServerApp


class HomeAssistant(HomeServerApp):
    @property
    def config_file(self):
        return self.path / 'config' / 'configuration.yaml'

    def setup(self):
        """Setup home assistant base url."""
        self.container.stop()
        self.setup_nginx()
        self.container.start()

    def setup_nginx(self):
        """Setup base url to use it as a proxy server. It requires the FULL url."""
        config = self.config_file.read_text()
        if not 'base_url' in config:
            config += f"http:\n  base_url: https://{self.domain}/homeassistant/"
        self.config_file.write_text(config)
