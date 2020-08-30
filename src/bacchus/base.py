from pathlib import Path
from time import sleep
import docker
import logging

TEMPLATES = Path(__file__).parent / 'templates'
DOCKER_PATH = Path(__file__).parent.parent.parent / 'docker'

logging.basicConfig(level=logging.INFO)


class HomeServerApp:
    """Base APP Class.

    All common actions (config file placement, docker controls...) go here
    """
    def __init__(self, domain, client, docker_prefix, compose, parent, **kwargs):
        self.service_name = self.__class__.__name__.lower()
        self.providers = parent.providers
        self.compose = compose
        self.path = DOCKER_PATH / 'data' / self.service_name
        self.domain = domain
        self.meta = kwargs
        self.meta['project_name'] = docker_prefix
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.path.mkdir(parents=True, exist_ok=True)
        self.client = client
        self.prefix = docker_prefix

    @property
    def running(self):
        return self.__class__.__name__.lower() in self.compose.services

    def container_for(self, service_name):
        return next((a for a in self.client.containers.list() if a.id == self.compose.get_service_id(service_name)))

    @property
    def container(self):
        return self.container_for(self.service_name)

    def wait_for_status(self):
        """Wait for container to start."""
        while not self.running:
            self.logger.debug(
                f'Waiting for {self.__class__.__name__} to start')
            sleep(1)

    def wait_for_config(self):
        """If we are waiting for a configuration file to be written, wait for it."""
        self.logger.debug(f'Waiting for {self.__class__.__name__} config')
        if hasattr(self, "config_file"):
            while not self.config_file.exists():
                sleep(1)
