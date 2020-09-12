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
        self.logger.debug('Setting up nginx paths')
        self.setup_paths()
        self.logger.debug('Installing external links apps')
        self.install_external_links()
        self.logger.debug('Setting up onlyoffice')
        self.setup_onlyoffice()
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
        """Install top links to all the rest of apps, to centralice everything on nextcloud"""
        self.occ('app:install', 'external')
        self.occ(
            'config:app:set', 'external', 'sites', '--value',
            json.dumps({
                "1": {
                    "id": 1,
                    "name": "Series downloads",
                    "url": f"https://private.{self.domain}/tv/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                },
                "2": {
                    "id": 2,
                    "name": "Movies downloads",
                    "url": f"https://private.{self.domain}/movies/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                },
                "3": {
                    "id": 3,
                    "name": "Music downloads",
                    "url": f"https://private.{self.domain}/music/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                },
                "4": {
                    "id": 4,
                    "name": "Book downloads",
                    "url": f"https://private.{self.domain}/books/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                },
                "5": {
                    "id": 5,
                    "name": "Media player",
                    "url": f"https://private.{self.domain}/jellyfin/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                }
            }))

    def setup_onlyoffice(self):
        trusted_domains = self.occ('config:system:get',
                                   'trusted_domains').splitlines()

        if not any([b'nginx' in a for a in trusted_domains]):
            self.logger.debug("Nginx not found in trusted domains, setting up")
            self.occ('config:system:set', 'trusted_domains',
                     str(len(trusted_domains)), '--value', 'nginx')

        self.logger.debug("Installing onlyoffice app")
        self.occ('app:install', 'onlyoffice')
        self.occ('config:system:set', 'onlyoffice', 'DocumentServerUrl',
                 '--value', '/ds-vpath/')
        self.occ('config:system:set', 'onlyoffice',
                 'DocumentServerInternalUrl', '--value',
                 'http://onlyoffice-document-server/')
        self.container_for('onlyoffice-document-server').exec_run([
            "sed", "-i",
            's/"rejectUnauthorized": true/"rejectUnauthroized": false/g',
            '/etc/onlyoffice/documentserver/default.json'
        ])
        self.occ('config:system:set', 'onlyoffice', 'StorageUrl', '--value',
                 'https://nginx/"')

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
        except:
            self.logger.exception('could not execute command')
