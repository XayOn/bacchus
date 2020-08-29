from bacchus.base import HomeServerApp


class CertManager(HomeServerApp):
    def setup(self):
        cmd = [
            '--dns', 'gandiv5', '-a', '-d', f'private.{self.domain}',
            '--email', f'{self.meta["nextcloud_username"]}', 'run'
        ]
        if (self.path / 'certificates' /
                f'private.{self.domain}.key').exists():
            self.logger.debug('Initial certificates already exists')
        else:
            self.logger.debug('Setting up certificates with lego')
            self.logger.debug(
                self.client.containers.run(
                    'goacme/lego',
                    command=cmd,
                    environment={'GANDIV5_API_KEY': self.meta['dns_api_key']},
                    volumes={
                        self.path.absolute(): {
                            'bind': '/.lego',
                            'mode': 'rw'
                        }
                    },
                    auto_remove=True,
                    detach=False))
            self.logger.debug('Set up certificates with lego')

    def wait_for_status(self):
        # Not actually needed...
        return True
