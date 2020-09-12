from pathlib import Path
import os
import shutil
import subprocess
import uuid

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
        root_pwd = uuid.uuid4().hex
        nextcloud_passwd = uuid.uuid4().hex
        (DOCKER_PATH / '.env_general').write_text(f"""PID={os.geteuid()}
    PUID={os.geteuid()}
    PGID={os.getegid()}""")
        (DOCKER_PATH /
         '.env_nextcloud').write_text(f"""NEXTCLOUD_ADMIN_USER=admin
    NEXTCLOUD_ADMIN_PASSWORD={nextcloud_passwd}
    NEXTCLOUD_UPDATE=1
    """)

    def copy_template(self):
        compose = (TEMPLATES / 'docker-compose.yml').read_text()
        if not Path('/dev/dri').exists():
            compose = compose.replace(""" devices:
      - /dev/dri:/dev/dri""", '')
        (DOCKER_PATH / 'docker-compose.yml').write_text(compose)


        # Hack to allow nginx docker config mount
        nginx_path = DOCKER_PATH / 'data' / 'nginx'
        nginx_path.mkdir(exist_ok=True, parents=True)
        (nginx_path / 'nginx.conf').write_text('')

    def start(self):
        """Start."""
        print(f'starting {self.meta["project_name"]}')
        subprocess.check_output(
            ['docker-compose', '-p', self.meta['project_name'], 'up', '-d'],
            cwd=DOCKER_PATH,
            env={
                **os.environ,
                **self.env
            })

    def stop(self):
        """Stop."""
        subprocess.check_output(['docker-compose', 'stop'],
                                cwd=DOCKER_PATH,
                                env=self.env)

    def get_service_id(self, name):
        return subprocess.check_output(['docker-compose', 'ps', '-q', name],
                                       cwd=DOCKER_PATH,
                                       env=self.env).strip().decode()
    def wait_for_status(self):
        pass

    def setup(self):
        pass

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
