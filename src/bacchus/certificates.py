from .base import HomeServerApp
import netifaces
import yaml

providers = {'ghandi': ['GHANDI_USERNAME', 'TOKEN']}


class CertManager(HomeServerApp):
    def setup_wildcard_certificate(self):
        data = {
            'delegate': 'wildcard',
            'ghandi': {
                'auth_token': self.meta['token'],
            }
        }
        nginx_name = self.containers['nginx'].name
        domain_cfg = f'*.{self.domain} autorestart-containers={nginx_name}'

        (self.path / 'lexicon.yml').write_text(
            yaml.dump(data, Dumper=yaml.CDumper))
        (self.path / 'domains.config').write_text(domain_cfg)

        try:
            result = self.client.containers.run(
                'adferrand/letsencrypt-dns',
                command=[
                    'lexicon', 'auto', 'create', self.domain, '--name',
                    'public', '--value', '$(curl https://api.ipify.org)'
                ],
                auto_remove=True,
                detach=False)
        except Exception as err:
            self.logger.exception('could not create public subdomain')

        try:
            default_iface = next(a for a in netifaces.interfaces()
                                 if a.startswith('enp') or a.startswith('eth'))
            private_ip = netifaces.ifaddresses(
                self.meta.get('iface', default_iface))[netifaces.AF_LINK]
            result = self.client.containers.run('adferrand/letsencrypt-dns',
                                                command=[
                                                    'lexicon', 'auto',
                                                    'create', self.domain,
                                                    '--name', 'private',
                                                    '--value',
                                                    private_ip[0]['addr']
                                                ],
                                                auto_remove=True,
                                                detach=False)
        except Exception as err:
            self.logger.exception('could not create public subdomain')

        try:
            # We create it here because we need to have pre-created the configs
            # and thus launched nginx one to get its name...
            result = self.client.containers.run(
                'adferrand/letsencrypt-dns',
                command=cmd,
                volumes={
                    '/var/run/docker.sock':
                    dict(bind='/var/run/docker.sock', mode='rw'),
                    self.path.absolute():
                    dict(bind='/etc/letsencrypt', mode='rw')
                },
                auto_remove=False,
                detach=False)
            self.logger.debug(result)
        except Exception as err:
            self.logger.exception('could not create ssl certs')
        self.logger.debug(list(data_path.glob('*')))
