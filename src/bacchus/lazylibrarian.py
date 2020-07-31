import configparser
from .base import HomeServerApp


class LazyLibrarian(HomeServerApp):
    @property
    def config_file(self):
        return self.path / 'config.ini'

    def setup_nginx(self):
        config = configparser.ConfigParser()
        config.read(str(self.config_file))
        config.set('General', 'http_root', '/books')
        config.set('General', 'ebook_dir', '/books')
        config.set('General', 'download_dir', '/downloads')
        with open(self.config_file, 'w') as fileo:
            config.write(fileo)

    def setup(self):
        if self.container:
            self.container.stop()
        self.setup_nginx()
        self.setup_indexers()
        self.compose.start()
