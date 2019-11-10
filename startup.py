#!/usr/bin/env python
from contextlib import suppress
from pathlib import Path
import subprocess
import os
import shutil
import sys

import jinja2

CREATE_CERT = ("certbot certonly --webroot -w /var/www/certbot --email {email}"
               " -d {domain} {staging} --rsa-key-size 4096 --agree-tos "
               "--force-renewal")


def init_letsencrypt(path, domain, email, staging):
    path = Path(path)

    # Cleanup and recreate directories.
    data_path = path / "data" / "certbot"
    with suppress(Exception):
        shutil.rmtree(data_path)
    data_path.mkdir(parents=True, exist_ok=True)
    (data_path / 'live' / domain).mkdir(parents=True, exist_ok=True)

    nginx_config = jinja2.Template((path / 'nginx.tpl').read_text())

    # Request certificate
    (path / 'data' / 'nginx.conf').write_text(
        nginx_config.render(init=True, domain=domain))
    create_cert = CREATE_CERT.format(email=email,
                                     domain=domain,
                                     staging='--staging' if staging else '')

    compose('run', 'certbot', create_cert) 

    # Write nginx config with new certificates
    (path / 'data' / 'nginx.conf').write_text(
        nginx_config.render(init=False, domain=domain))

    # Relaunch dockers.
    compose('up', '--force-recreate', '-d', 'nginx')
    compose('up', '-d')


def setup_onlyoffice():
    trusted_domains = occ('config:system:get', 'trusted_domains').splitlines()
    if not any(['nginx-server' in a for a in trusted_domains]):
        occ('config:system:set', 'trusted_domains', len(trusted_domains),
            '--value', 'nginx-server')

        occ('app:install', 'onlyoffice')
        occ('config:system:set', 'onlyoffice', 'DocumentServerUrl',
            '--value="/ds-vpath/"')
        occ('config:system:set', 'onlyoffice', 'DocumentServerInternalUrl',
            '--value="http://onlyoffice-document-server/"')
        occ('config:system:set', 'onlyoffice', 'StorageUrl',
            '--value="http://nginx-server/"')


def occ(*args):
    return compose('exec', '-u', 'www-data', 'nextcloud', 'php', 'occ',
                   '--no-warnings', *args)


def compose(command, *args):
    args = list(args)
    if command == 'run':
        args = ['-d', args[0], '--rm', '--entrypoint'] + args[1:]
    args = ['docker-compose', command] + args
    return subprocess.check_output(args)


def main(path, domain, email, staging):
    init_letsencrypt(path, domain, email, staging)
    setup_onlyoffice()


main(*sys.argv[1:])
