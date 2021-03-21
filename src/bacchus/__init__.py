import itertools
from time import sleep
import docker
from bacchus.compose import DockerCompose

from bacchus.arr import Radarr, Lidarr, Sonarr
from bacchus.dns import DNS
from bacchus.ombi import Ombi

from bacchus.nextcloud import NextCloud

from bacchus.jackett import Jackett
from bacchus.transmission import Transmission
from bacchus.openvpn import OpenVPN
from bacchus.jellyfin import Jellyfin

from cleo import Command
from cleo import Application

__all__ = [
    DockerCompose, DNS, Jackett, Transmission, Lidarr, Radarr, Sonarr,
    Jellyfin, Ombi, NextCloud, OpenVPN
]

CATEGORIES = {
    'base': [DNS, OpenVPN],
    'media_download': [Lidarr, Radarr, Sonarr, Transmission, Jackett],
    'media_management': [Jellyfin, Ombi],
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

        print('Waiting two minutes to start')
        sleep(60 * 2)
        compose.stop()

        for provider in providers:
            print(f'Setting up {provider.__class__.__name__} first step')
            provider.setup_first_step()

        compose.start()

        print('Waiting two minutes to start')
        sleep(60 * 2)
        for provider in providers:
            print(f'Setting up {provider.__class__.__name__} second step')
            provider.setup_second_step()


class InstallCommand(Command):
    """Installs bacchus

    install
        {--email=? : Your e-mail address}
        {--domain=? : Domain (FQDN) on gandi.net}
        {--dns=? : DNS Provider (gandi.net) API key}
        {--iface=? : (Optional) Main interface name}
        {--categories=? : (Optional) Set up specific categories}
        {--provider=? : (Optional) Set up only one service}
    """
    def handle(self):
        """Handle command"""
        setup = HomeServerSetup(domain=self.option('domain'),
                                email=self.option('email'),
                                iface=self.option('iface'),
                                dns_api_key=self.option('dns'))
        setup.configure(self.option('provider'), self.option('categories'))


def main():
    application = Application()
    application.add(InstallCommand())
    application.run()
