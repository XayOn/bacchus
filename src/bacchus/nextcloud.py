import json
import uuid
from .base import HomeServerApp


class NextCloud(HomeServerApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = uuid.uuid4().hex
        self.logger.info(
            f'Setting up admin password as "{self.password}", save it.')

    def setup(self):
        self.logger.debug('Fixing directory permissions permissions')
        self.fix_permissions()
        self.logger.debug('Installing nextcloud')
        self.install()
        self.logger.debug('Setting up paths')
        self.setup_paths()
        self.logger.debug('Installing external links apps')
        self.install_external_links()
        self.logger.debug('Installing apps')
        self.setup_apps()
        self.logger.debug('Set up nextcloud')

    def fix_permissions(self):
        self.container.exec_run(['chown', '-R', 'www-data', '/data'],
                                stdout=False,
                                privileged=True)

    def install(self):
        self.occ('maintenance:install', '--data-dir', '/data', '--admin-pass',
                 self.password, '--admin-user', 'admin')

    def setup_paths(self):
        self.occ('config:system:set', 'overwritewebroot', '--value', '/')
        self.occ('config:system:set', 'overwriteprotocol', '--value', 'https')
        self.occ('config:system:set', 'trusted_domains', '0', '--value',
                 f'private.{self.domain}')

    def setup_apps(self):
        apps = ('ocsms', 'tasks', 'calendar', 'deck', 'contacts', 'side_menu',
                'maps', 'breezedark')
        for app in apps:
            self.occ('app:install', app)

    def install_external_links(self):
        """Install top links to all the rest of apps"""
        self.occ('app:install', 'external')
        self.occ(
            'config:app:set', 'external', 'sites', '--value',
            json.dumps({
                "1": {
                    "id": 1,
                    "name": "Downloads management",
                    "url": f"https://private.{self.domain}/ombi/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                },
                "2": {
                    "id": 5,
                    "name": "Media player",
                    "url": f"https://private.{self.domain}/jellyfin/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                },
                "3": {
                    "id": 2,
                    "name": "Advanced download settings",
                    "url": f"https://private.{self.domain}/heimdall/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                }
            }))

    def occ(self, *args, **kwargs):
        try:
            args = ['php', 'occ', '--no-warnings', *args]
            kwargs.update(
                dict(user='www-data',
                     stdout=True,
                     demux=False,
                     stderr=False))
            result = self.container.exec_run(args, **kwargs)
            self.logger.debug(result)
            return result[1]
        except Exception:
            self.logger.exception('could not execute command')
