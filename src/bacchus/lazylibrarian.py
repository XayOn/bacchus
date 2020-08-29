import configparser
from .base import HomeServerApp


class LazyLibrarian(HomeServerApp):
    @property
    def config_file(self):
        return self.path / 'config.ini'

    def setup_nginx(self):
        self.container.stop()
        config = configparser.ConfigParser()
        config.read(str(self.config_file))
        config.set('General', 'HTTP_ROOT', '/books')
        with open(self.config_file, 'w') as fileo:
            config.write(fileo)
        self.compose.start()

    def setup(self):
        self.setup_nginx()
        config = configparser.ConfigParser()
        config.read(str(self.config_file))
        config.set('General', 'http_root', '/books')
        config.set('General', 'ebook_dir', '/books')
        config.set('General', 'download_dir', '/downloads')
        with open(self.config_file, 'w') as fileo:
            config.write(fileo)
