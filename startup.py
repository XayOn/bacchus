#!/usr/bin/env python
from contextlib import suppress
from functools import lru_cache
from pathlib import Path
from time import sleep
import configparser
import json
import logging
import os
import shutil
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET
import yaml

CREATE_TEMP = ()

logging.basicConfig(level=logging.DEBUG)


def create_env_file():
    root_pwd = uuid.uuid4().hex
    Path('.env_general').write_text(f"""PID={os.geteuid()}
PGID={os.getegid()}""")
 
    Path('.env_nextcloud').write_text(f"""NEXTCLOUD_ADMIN_USER=admin
NEXTCLOUD_ADMIN_PASSWORD=admin
NEXTCLOUD_UPDATE=1
""")


def compose(command, *args):
    args = list(args)
    if command == 'run':
        args = ['-d', args[0], '--rm', '--entrypoint'] + args[1:]
    args = ['docker-compose', command] + args
    try:
        return subprocess.check_output(args)
    except subprocess.CalledProcessError as excp:
        logging.error(excp.output)
    except Exception as excp:
        logging.exception(excp)


class App:
    def __init__(self, path, domain):
        self.path = Path(path)
        self.domain = domain


class Radarr(App):
    @property
    def config_file(self):
        return (self.path / 'data' / 'radarr' / 'config.xml').absolute()

    @property
    @lru_cache()
    def config(self):
        return ET.parse(str(self.config_file))

    def setup_nginx(self):
        self.config.find('UrlBase').text = '/movies'
        self.config.write(str(self.config_file))

    def setup(self):
        logging.debug("Setting up nginx")
        self.setup_nginx()
        logging.debug("Saved config %s", self.config_file)


class Lidarr(App):
    @property
    def config_file(self):
        return (self.path / 'data' / 'lidarr' / 'config.xml').absolute()

    @property
    @lru_cache()
    def config(self):
        return ET.parse(str(self.config_file))

    def setup_nginx(self):
        self.config.find('UrlBase').text = '/music/'
        self.config.write(str(self.config_file))

    def setup(self):
        logging.debug("Setting up nginx")
        self.setup_nginx()
        logging.debug("Saved config %s", self.config_file)


class Medusa(App):
    @property
    def config_file(self):
        return (self.path / 'data' / 'medusa' / 'config.ini').absolute()

    def setup_nginx(self):
        config = configparser.ConfigParser()
        config.read(str(self.config_file))
        config.set('General', 'web_root', '/tv')
        with open(self.config_file, 'w') as fileo:
            config.write(fileo)

    def setup(self):
        logging.debug("Setting up medusa")
        self.setup_nginx()
        logging.debug("Set up %s", self.config_file)


class NextCloud(App):
    def setup(self):
        compose('up', '-d')
        self.install()
        self.setup_onlyoffice()
        compose('stop')

    def install(self):
        compose('exec', 'nextcloud', 'chown', '-R', 'www-data', '/data')
        self.occ('maintenance:install', '--data-dir', '/data', '--admin-pass', 'admin', '--admin-user', 'admin')
        self.occ('config:system:set', 'overwritewebroot', '--value',
                 '/nextcloud')
        self.occ('config:system:set', 'overwriteprotocol', '--value', 'https')
        self.occ('config:system:set', 'trusted_domains', '0', '--value',
                 self.domain)

    def setup_onlyoffice(self):
        logging.debug('setting_onlyoffice')
        trusted_domains = self.occ('config:system:get',
                                   'trusted_domains').splitlines()

        if not any([b'nginx' in a for a in trusted_domains]):
            self.occ('config:system:set', 'trusted_domains',
                     str(len(trusted_domains)), '--value', 'nginx')

        self.occ('app:install', 'onlyoffice')
        self.occ('config:system:set', 'onlyoffice', 'DocumentServerUrl',
                 '--value', '/ds-vpath/')
        self.occ('config:system:set', 'onlyoffice',
                 'DocumentServerInternalUrl',
                 '--value', 'http://onlyoffice-document-server/')
        self.occ('config:system:set', 'onlyoffice', 'StorageUrl',
                 '--value', 'http://nginx/"')

    @staticmethod
    def occ(*args):
        try:
            return compose('exec', '-u', 'www-data', 'nextcloud', 'php', 'occ',
                           '--no-warnings', *args)
        except:
            pass


class HomeAssistant(App):
    def setup(self):
        """Setup home assistant base url."""
        logging.debug("Setting up jackett")
        self.setup_nginx()
        logging.debug("Set up %s", self.config_file)

    def setup_nginx(self):
        cfgdir = self.path / 'data' / 'homeassistant' / 'config'
        config = (cfgdir / 'configuration.yaml').read_text()
        if not 'base_url' in config:
            config += f"http:\n  base_url: https://{self.domain}/homeassistant/"

        with open(str(cfgdir / 'configuration.yaml')) as fileo:
            fileo.write(config)


class Jackett(App):
    def setup(self):
        logging.debug("Setting up jackett")
        self.setup_nginx()
        logging.debug("Set up ServerConfig")

    def setup_nginx(self):
        config = self.path / 'data' / 'jackett' / 'Jackett' / 'ServerConfig.json'
        result = json.load(config.open())
        result['BasePathOverride'] = '/trackers'
        json.dump(result, config.open('w'))


class Nginx:
    def __init__(self, path, domain):
        self.path = Path(path)
        self.domain = domain

    def setup(self):
        # Cleanup and recreate directories.
        domain = self.domain
        data_path = self.path / "data" / "certs" / domain
        if not data_path.exists():
            data_path.mkdir(parents=True, exist_ok=True)
            subprocess.check_output(
                f"docker run -v\"{data_path.parent.absolute()}:/etc/certs\" "
                f"frapsoft/openssl req -x509 -nodes -newkey rsa:4096 "
                f"-days 365 -keyout "
                f"'/etc/certs/{domain}/privkey.pem' -out "
                f"'/etc/certs/{domain}/fullchain.pem' "
                f"-subj '/CN=localhost'",
                shell=True)

        # Write nginx config
        (self.path / 'data' / 'nginx.conf').write_text(
            (self.path / 'nginx.tpl').read_text().format(domain=domain))
        compose('up', '-d')
        sleep(60 * 2)
        compose('stop')


if __name__ == "__main__":
    create_env_file()
    if len(sys.argv) == 4:
        app = [app for app in App.__subclasses__() if app.__name__ == sys.argv[3]][0]
        try:
            app(sys.argv[1], sys.argv[2]).setup()
        except Exception as err:
            logging.exception(err)
    else:
        Nginx(*sys.argv[1:3]).setup()
        for app in App.__subclasses__():
            try:
                app(*sys.argv[1:]).setup()
            except Exception as err:
                logging.exception(err) 
    compose('up', '-d')
