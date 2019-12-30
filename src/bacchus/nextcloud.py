import json
from .base import HomeServerApp


class NextCloud(HomeServerApp):
    def setup(self):
        self.fix_permissions()
        self.install()
        self.create_users()
        self.setup_paths()
        self.install_external_links()
        self.setup_onlyoffice()

    def fix_permissions(self):
        self.container_exec_run('chown',
                                '-R',
                                'www-data',
                                '/data',
                                privileged=True)

    def install(self):
        self.occ('maintenance:install', '--data-dir', '/data', '--admin-pass',
                 'admin', '--admin-user', 'admin')

    def create_users(self):
        self.occ('user:add',
                 '--password-from-env',
                 '--display-name',
                 self.meta['nextcloud_username'],
                 '1',
                 environment={'OC_PASS': self.meta['nextcloud_password']})

    def setup_paths(self):
        self.occ('config:system:set', 'overwritewebroot', '--value', '/')
        self.occ('config:system:set', 'overwriteprotocol', '--value', 'https')
        self.occ('config:system:set', 'trusted_domains', '0', '--value',
                 self.domain)

    def install_external_links(self):
        """Install top links to all the rest of apps, to centralice everything on nextcloud"""
        self.occ('app:install', 'external')
        self.occ(
            'docker-docker', 'exec', '-u', 'www-data', 'nextcloud', 'php',
            'occ', 'config:app:set', 'external', 'sites',
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
        self.occ('user:add')

    def setup_onlyoffice(self):
        trusted_domains = self.occ('config:system:get',
                                   'trusted_domains').splitlines()

        if not any([b'nginx' in a for a in trusted_domains]):
            self.occ('config:system:set', 'trusted_domains',
                     str(len(trusted_domains)), '--value', 'nginx')

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
            self.container.exec_run(*args,
                                    stdout=False,
                                    stderr=False,
                                    user='www-data',
                                    **kwargs)
        except:
            self.logger.exception('could not execute command')
