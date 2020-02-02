from bacchus.certificates import CertManager
from bacchus.compose import DockerCompose
from bacchus.jackett import Jackett
from bacchus.jellyfin import Jellyfin
from bacchus.lidarr import Lidarr
from bacchus.medusa import Medusa
from bacchus.nextcloud import NextCloud
from bacchus.nginx import Nginx
from bacchus.openvpn import OpenVPN
from bacchus.radarr import Radarr
import docker

__all__ = [
    Nginx, CertManager, NextCloud, Jackett, Lidarr, Radarr, Medusa, Jellyfin
]


class HomeServerSetup:
    """Base cmdline class. 

    Not currently extending a CLEO App so this can be extended easily.
    Params are the same as BaseHomeApp class from `base` module.
    """
    def __init__(self, domain, docker_prefix="bacchus", **kwargs):
        """Setup providers.

        Kwargs will be inherited as metadata, for example, nextcloud will use the nextcloud_username
        and nextcloud_password variables
        """
        client = docker.from_env()
        self.compose = DockerCompose(domain, client, docker_prefix, None,
                                     **kwargs)
        self.providers = {
            cls.__name__: cls(domain, client, docker_prefix, self.compose,
                              self, **kwargs)
            for cls in __all__
        }

    def configure(self, provider_names=None):
        """Configure given providers."""
        if not provider_names:
            provider_names = [a.__name__ for a in __all__]

        self.compose.copy_template()
        self.compose.create_env_files()
        self.compose.start()

        for provider in provider_names:
            self.providers[provider].wait_for_status()
            self.providers[provider].wait_for_config()
            self.providers[provider].setup()
        self.compose.restart()
