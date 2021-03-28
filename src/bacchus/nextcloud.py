import json
import uuid
from .base import HomeServerApp


class NextCloud(HomeServerApp):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.password = uuid.uuid4().hex
        self.logger.info(
            f'Setting up admin password as "{self.password}", save it.')

    def setup_second_step(self):
        self.fix_permissions()
        self.install()
        self.setup_paths()
        self.setup_apps()

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
                 f'cloud.{self.domain}')

    def setup_apps(self):
        apps = ('ocsms', 'tasks', 'calendar', 'deck', 'contacts', 'breezedark')
        for app in apps:
            self.occ('app:install', app)

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
