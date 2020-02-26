import configparser
import json
from .base import TEMPLATES
from .base import HomeServerApp


class Medusa(HomeServerApp):
    @property
    def config_file(self):
        return self.path / 'config.ini'

    def setup_nginx(self):
        config = configparser.ConfigParser()
        config.read(str(self.config_file))
        config.set('General', 'web_root', '/tv')
        with open(self.config_file, 'w') as fileo:
            config.write(fileo)

    def setup_indexers(self):
        config = configparser.ConfigParser()
        config.read(str(self.config_file))
        api_key = json.loads((self.path / '..' / 'jackett' / 'Jackett' /
                              'ServerConfig.json').read_text())['APIKey']

        providers = []
        for prov in (TEMPLATES / 'jackett' / 'Indexers').glob('*.json'):
            providers.append(prov.stem.lower())
            local = dict(
                name=prov.stem,
                cat_ids=('5010, 5030, 5040, 2000, 2010, '
                         '2020, 2030, 2035, 2040, 2045, 2050, 2060'),
                api_key=api_key,
                search_mode='eponly',
                search_fallback=0,
                enable_daily=1,
                enable_backlog=1,
                enable_manualsearch=1,
                enable_search_delay=0,
                ratio='',
                search_delay=480,
                minseed=1,
                url=(f'https://private.{self.domain}/trackers/api/v2.0/'
                     f'indexers/{prov.stem}/results/torznab/'))
            if not config.has_section(prov.stem.upper()):
                config.add_section(prov.stem.upper())
            config[prov.stem.upper()].update({
                f'{prov.stem}_{prop}': str(val)
                for prop, val in local.items()
            })
            config[prov.stem.upper()][prov.stem.lower()] = '1'

            if not config.has_section('TORRENT'):
                config.add_section('TORRENT')

            config['TORRENT'].update(
                dict(torrent_username='',
                     torrent_password='',
                     torrent_host=f'https://{self.domain}',
                     torrent_path='',
                     torrent_seed_time='3',
                     torrent_paused='0',
                     torrent_high_bandwidth='0',
                     torrent_label='',
                     torrent_label_anime='',
                     torrent_verify_cert='0',
                     torrent_rpcurl='transmission/rpc',
                     torrent_auth_type='',
                     torrent_seed_location=''))

        config['Torznab']['torznab_providers'] = ','.join(providers)

        with open(self.config_file, 'w') as fileo:
            config.write(fileo)

    def setup(self):
        if self.container:
            self.container.stop()
        self.setup_nginx()
        self.setup_indexers()
        self.compose.start()
