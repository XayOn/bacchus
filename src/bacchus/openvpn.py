from contextlib import suppress
from bacchus.base import HomeServerApp


class OpenVPN(HomeServerApp):
    def setup_first_step(self):
        try:
            self.logger.debug(
                self.run("ovpn_genconfig", "-u",
                         f"udp://public.{self.domain}"))
            with suppress(Exception):
                self.logger.debug(
                    self.run('bash', '-c',
                             f'echo public.{self.domain}|ovpn_initpki nopass'))

            self.compose.start()
            with suppress(Exception):
                self.logger.debug(
                    self.run('easyrsa', 'build-client-full',
                             self.meta['email'], 'nopass'))
            response = self.run('ovpn_getclient',
                                self.meta['email'])
            (self.path / '..' / 'openvpn_client.conf').write_bytes(response)
        except Exception:
            self.logger.exception('could not create openvpn config')

        try:
            self.fix_dns_config_pihole()
        except Exception:
            self.logger.exception('cant_dns_pihole')

    def fix_dns_config_pihole(self):
        server_config = [
            a for a in (self.path / 'openvpn.conf').open().readlines()
            if 'dhcp-option DNS' not in a
        ] + ['push "dhcp-option DNS 127.0.0.1"']
        # TODO: Use docker cp or api...
        (self.path / 'openvpn.conf').write_text('\n'.join(server_config))

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
