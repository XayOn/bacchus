from pathlib import Path
from bacchus.base import HomeServerApp


class OpenVPN(HomeServerApp):
    def setup(self):
        try:
            self.logger.debug(
                self.run("ovpn_genconfig", "-u", f"udp://{self.domain}"))
            self.logger.debug(
                self.run('bash', '-c',
                         f'echo {self.domain}|ovpn_initpki nopass'))
            # self.container.stop()
            self.compose.start()
            self.logger.debug(
                self.run('easyrsa', 'build-client-full',
                         self.meta['nextcloud_username'], 'nopass'))
            response = self.run('ovpn_getclient',
                                self.meta['nextcloud_username'])
            Path('vpn_client.config').write_text(response)
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
