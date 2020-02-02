from cleo import Command
from cleo import Application

from . import HomeServerSetup


class GreetCommand(Command):
    """
    Installs bacchus 

    install
        {domain? : Domain (FQDN) for virtualhosts} 
        {username? : Nextcloud first user's username}
        {password? : Nextcloud first user's password}
        {iface? : (Optional) Main interface name} 
        {provider? : (Optional) Set up only one service} 
    """
    def handle(self):
        """Handle command"""
        setup = HomeServerSetup(domain=self.argument('domain'),
                                iface=self.argument('iface'),
                                nextcloud_username=self.argument('username'),
                                nextcloud_password=self.argument('password'))

        setup.configure(self.argument('provider'))


def main():
    application = Application()
    application.add(GreetCommand())
    application.run()
