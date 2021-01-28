from .base import HomeServerApp
import netifaces as ni
import requests


class DNS(HomeServerApp):
    def create_dns(self, domain, addr):
        cmd = [
            "lexicon", "gandi", "create", self.domain, "A", "--auth-token",
            self.meta['dns_api_key'], "--api-protocol", "rest", '--name',
            domain, '--content', addr
        ]
        self.logger.debug(f'Executing {cmd}')

        return self.client.containers.run('analogj/lexicon',
                                          command=cmd,
                                          auto_remove=True,
                                          detach=False)

    def setup_first_step(self):
        default_iface = next(a for a in ni.interfaces() if any(
            a.startswith(b) for b in ('eth', 'en')))
        iface = self.meta.get('iface') or default_iface
        private_ip = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
        public_ip = requests.get('https://api.ipify.org').text
        self.logger.debug(
            f'Setting up public and private for {public_ip}, {private_ip}')
        self.logger.debug(self.create_dns('public', public_ip))
        self.logger.debug('Finished public config')
        self.logger.debug(self.create_dns('private', private_ip))
        self.logger.debug('Finished private config')
