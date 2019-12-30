from pathlib import Path
from time import sleep
import docker

TEMPLATES = Path(__file__).parent / 'templates'
DOCKER_PATH = Path(__file__).parent / 'docker'


class HomeServerApp:
    """Base APP Class.

    All common actions (config file placement, docker controls...) go here
    """
    def __init__(self, domain, client, docker_prefix, **kwargs):
        name = self.__class__.__name__.lower()
        self.path = DOCKER_PATH / 'data' / name
        self.domain = domain
        self.meta = kwargs
        self.meta['project_name'] = docker_prefix
        self.path.mkdir(parents=True, exist_ok=True)
        self.client = client
        self.prefix = docker_prefix

    @property
    def containers(self):
        """Return a list of all containers associated with current docker"""
        return {
            a.name.replace(self.prefix, ''): a
            for a in self.client.containers.list()
            if a.name.startswith(self.prefix)
        }

    @property
    def container(self):
        return self.containers[self.__class__.__name__.lower()]

    @property
    def running(self):
        return self.container.status == 'running'

    def wait_for_status(self):
        """Wait for container to start."""
        while not self.running:
            sleep(1)

    def wait_for_config(self):
        """If we are waiting for a configuration file to be written, wait for it."""
        if hasattr(self, "config_file"):
            while not self.config_file.exists():
                sleep(1)
