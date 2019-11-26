#!/usr/bin/env python
import configparser
from contextlib import suppress
from pathlib import Path
import subprocess
import os
import shutil
import sys

CREATE_TEMP = ()


class App:
    def __init__(self, path):
        self.path = path


class Medusa(App):
    def setup(self):
        config = configparser.ConfigParser()
        config.read(self.path / 'data' / 'medusa' / 'config.ini')
        config['General']['web-root'] = '/tv'
        config.save()


def init_nginx(path, domain):
    path = Path(path)

    # Cleanup and recreate directories.
    data_path = path / "data" / "certs" / domain
    if not data_path.exists():
        data_path.mkdir(parents=True, exist_ok=True)
        subprocess.check_output(
            f"docker run -v{data_path.parent.absolute()}:/etc/certs "
            f"frapsoft/openssl req -x509 -nodes -newkey rsa:4096 "
            f"-days 365 -keyout "
            f"'/etc/certs/{domain}/privkey.pem' -out "
            f"'/etc/certs/{domain}/fullchain.pem' "
            f"-subj '/CN=localhost'",
            shell=True)

    # Write nginx config
    (path / 'data' / 'nginx.conf').write_text(
        (path / 'nginx.tpl').read_text().format(domain=domain))


def setup_onlyoffice():
    trusted_domains = occ('config:system:get', 'trusted_domains').splitlines()
    if not any(['nginx' in a for a in trusted_domains]):
        occ('config:system:set', 'trusted_domains', len(trusted_domains),
            '--value', 'nginx')

        occ('app:install', 'onlyoffice')
        occ('config:system:set', 'onlyoffice', 'DocumentServerUrl',
            '--value="/ds-vpath/"')
        occ('config:system:set', 'onlyoffice', 'DocumentServerInternalUrl',
            '--value="http://onlyoffice-document-server/"')
        occ('config:system:set', 'onlyoffice', 'StorageUrl',
            '--value="http://nginx/"')


def occ(*args):
    return compose('exec', '-u', 'www-data', 'nextcloud', 'php', 'occ',
                   '--no-warnings', *args)


def compose(command, *args):
    args = list(args)
    if command == 'run':
        args = ['-d', args[0], '--rm', '--entrypoint'] + args[1:]
    args = ['docker-compose', command] + args
    return subprocess.check_output(args)


def setup_apps(path):
    for app in App.__subclasses__():
        app(path).setup()


def main(path, domain):
    init_nginx(path, domain)
    compose('up', '-d')
    compose('down')
    setup_apps(path)
    setup_onlyoffice()


main(*sys.argv[1:])
