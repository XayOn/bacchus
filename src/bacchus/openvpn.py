import netifaces as ni
from contextlib import suppress
from pathlib import Path
from bacchus.base import HomeServerApp

import requests


class OpenVPN(HomeServerApp):
    def setup(self):
        self.setup_dns()
        try:
            self.logger.debug(
                self.run("ovpn_genconfig", "-u",
                         f"udp://public.{self.domain}"))
            with suppress(Exception):
                self.logger.debug(
                    self.run(
                        'bash', '-c',
                        f'echo public.{self.domain}|ovpn_initpki nopass'))

            self.compose.start()
            with suppress(Exception):
                self.logger.debug(
                    self.run('easyrsa', 'build-client-full',
                             self.meta['nextcloud_username'], 'nopass'))
            response = self.run('ovpn_getclient',
                                self.meta['nextcloud_username'])
            Path('vpn_client.config').write_bytes(response)
        except Exception as err:
            self.logger.exception('could not create openvpn config')

    def run(self, *cmd):
        volumes = {
            self.path.absolute(): {
                'bind': '/etc/openvpn',
                'mode': 'rw'
            }
        }
        return self.client.containers.run('kylemanna/openvpn',
                                          command=cmd,
                                          tty=True,
                                          volumes=volumes,
                                          detach=False)

    def setup_dns(self):
        default_iface = next(a for a in ni.interfaces() if any(
            a.startswith(b) for b in ('eth', 'enp')))
        iface = self.meta.get('iface') or default_iface
        private_ip = ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
        public_ip = requests.get('https://api.ipify.org').text
        self.logger.debug(
            f'Setting up public and private for {public_ip}, {private_ip}')
        self.logger.debug(self.create_dns('public', public_ip))
        self.logger.debug('Finished public config')
        self.logger.debug(self.create_dns('private', private_ip))
        self.logger.debug('Finished private config')

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

    def wait_for_status(self):
        return True
