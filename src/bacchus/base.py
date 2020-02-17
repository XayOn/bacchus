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
        name = self.__class__.__name__.lower()
        self.providers = parent.providers
        self.compose = compose
        self.path = DOCKER_PATH / 'data' / name
        self.domain = domain
        self.meta = kwargs
        self.meta['project_name'] = docker_prefix
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        self.path.mkdir(parents=True, exist_ok=True)
        self.client = client
        self.prefix = docker_prefix

    @property
    def containers(self):
        """Return a list of all containers associated with current docker"""
        return {
            a.name.split('_')[1]: a
            for a in self.client.containers.list()
            if a.name.split('_')[0] == self.prefix
        }

    @property
    def container(self):
        return self.containers.get(self.__class__.__name__.lower())

    @property
    def running(self):
        if not self.container:
            return False
        return self.container.status == 'running'

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
