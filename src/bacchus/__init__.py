import docker
# from bacchus.homeassistant import HomeAssistant
from bacchus.jackett import Jackett
from bacchus.transmission import Transmission
from bacchus.lidarr import Lidarr
from bacchus.radarr import Radarr
from bacchus.medusa import Medusa
from bacchus.nextcloud import NextCloud
from bacchus.nginx import Nginx
from bacchus.compose import DockerCompose
from bacchus.openvpn import OpenVPN
from bacchus.jellyfin import Jellyfin
from bacchus.certificates import CertManager

__all__ = [
    CertManager, Nginx, OpenVPN, NextCloud, Transmission, Jackett, Lidarr,
    Radarr, Medusa, Jellyfin
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
        self.providers = {}
        self.compose = DockerCompose(domain, client, docker_prefix, None, self,
                                     **kwargs)
        self.providers.update({
            cls.__name__: cls(domain, client, docker_prefix, self.compose,
                              self, **kwargs)
            for cls in __all__
        })

    def configure(self, provider_name=None):
        """Configure given providers."""
        if provider_name:
            return self.providers[provider_name].setup()

        self.compose.copy_template()
        self.compose.create_env_files()
        self.compose.start()

        for provider in self.providers.values():
            provider.wait_for_status()
            provider.wait_for_config()
            provider.setup()
        self.compose.restart()
