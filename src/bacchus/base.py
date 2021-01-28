from pathlib import Path
from time import sleep
import logging

TEMPLATES = Path(__file__).parent / 'static'
DOCKER_PATH = Path(__file__).parent.parent.parent / 'docker'

logging.basicConfig(level=logging.INFO)


class HomeServerApp:
    """Base APP Class.

    All common actions (config file placement, docker controls...) go here
    """
    def __init__(self, domain, parent, **kwargs):
        self.service_name = self.__class__.__name__.lower()
        self.providers = parent.providers
        self.parent = parent
        self.path = DOCKER_PATH / 'data' / self.service_name
        self.domain = domain
        self.meta = kwargs
        self.meta['project_name'] = 'bacchus'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.path.mkdir(parents=True, exist_ok=True)
        self.client = parent.client

    def container_for(self, service_name):
        return next((a for a in self.client.containers.list()
                     if a.id == self.compose.get_service_id(service_name)))

    @property
    def container(self):
        return self.container_for(self.service_name)

    @property
    def compose(self):
        return self.providers.get('DockerCompose')

    def setup_first_step(self):
        """Setup after first boot-and-wait"""

    def setup_second_step(self):
        """Setup after restart."""
