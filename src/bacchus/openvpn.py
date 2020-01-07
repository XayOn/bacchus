import tempfile
from bacchus.base import BaseHomeApp


class OpenVPN(BaseHomeApp):
    def setup(self):
        try:
            self.logger.debug(
                self.run("ovpn_genconfig"
                         "-u", f"udp://{self.host}"))
            self.logger.debug(self.run('ovpn_initpki'))
            self.container.stop()
            self.compose.start()
            self.logger.debug(
                self.run('easyrsa', 'build-client-full',
                         self.meta['nextcloud_username'], 'nopass'))
            response = self.run('ovpn_getclient',
                                self.meta['nextcloud_username'])
            with open(self.path / 'vpn_client.config') as fileo:
                fileo.write(response)
        except Exception as err:
            self.logger.exception('could not create openvpn config')

    def run(self, *cmd):
        volumes = {
            self.path.absolute(): {
                'bind': '/etc/openvpn',
                'mode': 'rw'
            }
        }
        return self.client.containers.run('frapsoft/openssl',
                                          command=cmd,
                                          volumes=volumes,
                                          auto_remove=True,
                                          detach=False)
