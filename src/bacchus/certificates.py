from bacchus.base import HomeServerApp


class CertManager(HomeServerApp):
    def setup(self):
        cmd = [
            '--dns', 'gandiv5', '-a', '-d', f'private.{self.domain}',
            '--email', f'{self.meta["email"]}', 'run'
        ]
        if (self.path / 'certificates' /
                f'private.{self.domain}.key').exists():
            self.logger.debug('Initial certificates already exists')
        else:
            self.logger.debug('Setting up certificates with lego')
            try:
                self.logger.debug(
                    self.client.containers.run('goacme/lego',
                                               command=cmd,
                                               environment={
                                                   'GANDIV5_API_KEY':
                                                   self.meta['dns_api_key']
                                               },
                                               volumes={
                                                   self.path.absolute(): {
                                                       'bind': '/.lego',
                                                       'mode': 'rw'
                                                   }
                                               },
                                               detach=False))
            except Exception as err:
                print(err)

            self.logger.debug('Set up certificates with lego')

    def wait_for_status(self):
        # Not actually needed...
        return True
