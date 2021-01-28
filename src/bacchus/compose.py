import os
import shutil
import subprocess
import uuid
from pathlib import Path

from .base import HomeServerApp
from .base import DOCKER_PATH
from .base import TEMPLATES


class DockerCompose(HomeServerApp):
    """Basic docker compose commands."""
    @property
    def env(self):
        return {
            **os.environ, 'COMPOSE_PROJECT_NAME': self.meta['project_name']
        }

    def create_env_files(self):
        """Create environment files for docker copose"""
        nextcloud_passwd = uuid.uuid4().hex

        gen = f"PID={os.geteuid()}\nPUID={os.geteuid()}\nPGID={os.getegid()}"
        gandi = f"GANDIV5_API_KEY={self.meta['dns_api_key']}"
        nextcloud = f"""NEXTCLOUD_ADMIN_USER=admin
NEXTCLOUD_ADMIN_PASSWORD={nextcloud_passwd}
NEXTCLOUD_UPDATE=1"""

        (DOCKER_PATH / '.env_general').write_text(gen)
        (DOCKER_PATH / '.env_traefik').write_text(gandi)
        (DOCKER_PATH / '.env_nextcloud').write_text(nextcloud)
        (DOCKER_PATH / '.env_mariadb').write_text('')

    def copy_template(self):
        compose = (TEMPLATES / 'docker-compose.yml').read_text()
        compose = compose.replace('EMAIL', self.meta['email'])
        compose = compose.replace('HOST', self.domain)
        if not Path('/dev/dri').exists():
            compose = compose.replace(
                """ devices:
      - /dev/dri:/dev/dri""", '')
        (DOCKER_PATH / 'docker-compose.yml').write_text(compose)

    def start(self):
        """Start."""
        print(f'starting {self.meta["project_name"]}')
        subprocess.check_output(
            ['docker-compose', '-p', self.meta['project_name'], 'up', '-d'],
            cwd=DOCKER_PATH,
            env={**os.environ, **self.env})

    def stop(self):
        """Stop."""
        subprocess.check_output(['docker-compose', 'stop'],
                                cwd=DOCKER_PATH,
                                env=self.env)

    def get_service_id(self, name):
        return subprocess.check_output(['docker-compose', 'ps', '-q', name],
                                       cwd=DOCKER_PATH,
                                       env=self.env).strip().decode()

    @property
    def services(self):
        services = [
            a.strip() for a in subprocess.check_output(
                ['docker-compose', 'ps', '--services'],
                cwd=DOCKER_PATH,
                env=self.env).decode().splitlines()
        ]
        return services

    def restart(self):
        self.stop()
        self.start()
