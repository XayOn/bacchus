import itertools
from time import sleep
import docker
from bacchus.compose import DockerCompose

from bacchus.lidarr import Lidarr
from bacchus.radarr import Radarr
from bacchus.dns import DNS
from bacchus.sonarr import Sonarr

from bacchus.nextcloud import NextCloud

from bacchus.jackett import Jackett
from bacchus.transmission import Transmission
from bacchus.openvpn import OpenVPN
from bacchus.jellyfin import Jellyfin

__all__ = [
    DockerCompose, DNS, Lidarr, Radarr, Sonarr, NextCloud, Jackett,
    Transmission, OpenVPN, Jellyfin
]

CATEGORIES = {
    'base': [DNS, OpenVPN],
    'media_download': [Lidarr, Radarr, Sonarr, Transmission, Jackett],
    'media_management': [Jellyfin],
    'cloud': [NextCloud]
}


class HomeServerSetup:
    """Base cmdline class.

    Not currently extending a CLEO App so this can be extended easily.
    Params are the same as BaseHomeApp class from `base` module.
    """
    def __init__(self, domain, **kwargs):
        """Setup providers.

        Kwargs will be inherited as metadata
        """
        self.client = docker.from_env()
        # tree-like, both compose (wich itself is a provider) and providers
        # need access to each other, so we'd do that trough the parent.
        self.providers = {}
        self.providers.update(
            {cls.__name__: cls(domain, self, **kwargs)
             for cls in __all__})

    def configure(self, provider_name=None, categories=None):
        """Configure given providers."""
        compose = self.providers['DockerCompose']

        compose.copy_template()
        compose.create_env_files()
        compose.start()

        if provider_name:
            providers = [self.providers[provider_name]]
        elif categories:
            providers = list(
                itertools.chain.from_iterable(
                    [CATEGORIES[b] for b in categories]))
        else:
            providers = self.providers.values()

        self.selected_providers = [a.__class__.__name__ for a in providers]
        self.selected_categories = categories

        sleep(60 * 2)
        compose.stop()

        for provider in providers:
            provider.setup_first_step()

        compose.start()

        sleep(60 * 2)
        for provider in providers:
            provider.setup_second_step()
