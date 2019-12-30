import json
from .base import HomeServerApp


class NextCloud(HomeServerApp):
    def setup(self):
        self.logger.debug('Fixing directory permissions permissions')
        self.fix_permissions()
        self.logger.debug('Installing nextcloud')
        self.install()
        self.logger.debug('Creating new user')
        self.create_users()
        self.logger.debug('Setting up nginx paths')
        self.setup_paths()
        self.logger.debug('Installing external links apps')
        self.install_external_links()
        self.logger.debug('Setting up onlyoffice')
        self.setup_onlyoffice()
        self.logger.debug('Set up nextcloud')

    def fix_permissions(self):
        self.container.exec_run(['chown', '-R', 'www-data', '/data'],
                                stdout=False,
                                privileged=True)

    def install(self):
        self.occ('maintenance:install', '--data-dir', '/data', '--admin-pass',
                 'admin', '--admin-user', 'admin')

    def create_users(self):
        self.occ('user:add', '--password-from-env', '--display-name',
                 self.meta['nextcloud_username'], '1')

    def setup_paths(self):
        self.occ('config:system:set', 'overwritewebroot', '--value', '/')
        self.occ('config:system:set', 'overwriteprotocol', '--value', 'https')
        self.occ('config:system:set', 'trusted_domains', '0', '--value',
                 self.domain)

    def install_external_links(self):
        """Install top links to all the rest of apps, to centralice everything on nextcloud"""
        self.occ('app:install', 'external')
        self.occ(
            'config:app:set', 'external', 'sites',
            json.dumps({
                "1": {
                    "id": 1,
                    "name": "Series",
                    "url": f"https:\/\/{self.domain}\/tv\/",
                    "lang": "",
                    "type": "link",
                    "device": "",
                    "icon": "external.svg",
                    "groups": [],
                    "redirect": False
                },
                "2": {
                    "id": 2,
                    "name": "Movies",
                    "url": f"https:\/\/{self.domain}\/movies\/",
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
        self.occ('config:system:set', 'onlyoffice', 'StorageUrl', '--value',
                 'http://nginx/"')

    def occ(self, *args, **kwargs):
        try:
            args = ['php', 'occ', '--no-warnings', *args]
            kwargs.update(
                dict(user='www-data',
                     stdout=True,
                     demux=False,
                     stderr=False,
                     environment={'OC_PASS': self.meta['nextcloud_password']}))
            result = self.container.exec_run(args, **kwargs)
            self.logger.debug(result)
            return result[1]
        except:
            self.logger.exception('could not execute command')
