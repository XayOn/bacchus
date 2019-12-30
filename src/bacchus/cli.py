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
    """
    def handle(self):
        """Handle command"""
        # TODO: More verbosity...
        setup = HomeServerSetup(domain=self.argument('domain'),
                                nextcloud_username=self.argument('username'),
                                nextcloud_password=self.argument('password'))

        # TODO: Allow passing a specific provider
        setup.configure()


def main():
    application = Application()
    application.add(GreetCommand())
    application.run()
