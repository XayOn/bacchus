import itertools
import docker
from bacchus.jackett import Jackett
from bacchus.transmission import Transmission
from bacchus.lazylibrarian import LazyLibrarian
from bacchus.lidarr import Lidarr
from bacchus.radarr import Radarr
from bacchus.medusa import Medusa
from bacchus.nextcloud import NextCloud
from bacchus.nginx import Nginx
from bacchus.compose import DockerCompose
from bacchus.openvpn import OpenVPN
from bacchus.jellyfin import Jellyfin
from bacchus.lazylibrarian import LazyLibrarian
from bacchus.certificates import CertManager
from bacchus.kodi import Kodi
from bacchus.pihole import PiHole

__all__ = [
    DockerCompose, CertManager, Nginx, OpenVPN, NextCloud, Transmission,
    Jackett, Lidarr, LazyLibrarian, Radarr, Medusa, Jellyfin, Kodi, PiHole
]

CATEGORIES = {
    'base': [CertManager, Nginx, OpenVPN, PiHole],
    'media_download':
    [Jackett, Lidarr, LazyLibrarian, Radarr, Medusa, Transmission],
    'media_management': [Jellyfin],
    'media_player': [Kodi],
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
        self.providers.update({cls.__name__: cls(domain, self, **kwargs)
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

        for provider in providers:
            provider.wait_for_status()
            provider.wait_for_config()
            provider.setup()

        compose.restart()
