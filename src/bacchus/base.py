from pathlib import Path
import logging

TEMPLATES = Path(__file__).parent / 'static'
DOCKER_PATH = Path(__file__).parent.parent.parent / 'docker'

logging.basicConfig(level=logging.INFO)


class HomeServerApp:
    """Base APP Class."""
    def __init__(self, domain):
        self.service_name = self.__class__.__name__.lower()
        self.domain = domain
        self.path = '/data' / self.service_name
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)

    def setup_first_step(self):
        """Setup after first boot-and-wait"""
