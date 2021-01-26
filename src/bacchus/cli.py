from cleo import Command
from cleo import Application

from . import HomeServerSetup


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
