import itertools
import docker
from bacchus.compose import DockerCompose
from bacchus.certificates import CertManager

from bacchus.lidarr import Lidarr
from bacchus.radarr import Radarr
from bacchus.readarr import Readarr
from bacchus.sonarr import Sonarr
from bacchus.bazarr import Bazarr

from bacchus.nextcloud import NextCloud
from bacchus.nginx import Nginx

from bacchus.jackett import Jackett
from bacchus.transmission import Transmission
from bacchus.openvpn import OpenVPN
from bacchus.pihole import PiHole

from bacchus.jellyfin import Jellyfin
from bacchus.ubooquity import Ubooquity
from bacchus.homer import Homer
from bacchus.kodi import Kodi

__all__ = [
    DockerCompose, CertManager, Lidarr, Radarr, Readarr, Sonarr, Bazarr, NextCloud, Nginx, 
    Jackett, Transmission, OpenVPN, PiHole, Jellyfin, Kodi, Ubooquity, Homer
]

CATEGORIES = {
    'base': [CertManager, Nginx, OpenVPN, PiHole, Homer],
    'media_download': [Lidarr, Radarr, Readarr, Sonarr, Bazarr, Transmission, Jackett],
    'media_management': [Jellyfin, Ubooquity],
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
