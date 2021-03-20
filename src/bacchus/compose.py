import os
import uuid
import shutil
from subprocess import check_output

from .base import HomeServerApp
from .base import DOCKER_PATH
from .base import TEMPLATES


class DockerCompose(HomeServerApp):
    """Basic docker compose commands."""
    @property
    def env(self):
        proj = self.meta['project_name']
        return {**os.environ, 'COMPOSE_PROJECT_NAME': proj}

    def create_env_files(self):
        """Create environment files for docker copose"""
        (DOCKER_PATH / '.env').write_text(f"""NEXTCLOUD_ADMIN_USER=admin
NEXTCLOUD_ADMIN_PASSWORD={uuid.uuid4().hex}
NEXTCLOUD_UPDATE=1
GANDIV5_API_KEY={self.meta['dns_api_key']}
host={self.meta['host']}
email={self.meta['email']}
PID={os.geteuid()}
PUID={os.geteuid()}
PGID={os.getegid()}
""")

    def copy_template(self):
        shutil.copy(TEMPLATES / 'docker-compose.yml',
                    DOCKER_PATH / 'docker-compose.yml')

    def cmd(self, args):
        """Start."""
        args = ['docker-compose', *args]
        return check_output(args, cwd=DOCKER_PATH, env=self.env)

    def start(self):
        return self.cmd(['up', '-d'])

    def stop(self):
        """Stop."""
        return self.cmd(['stop'])

    def get_service_id(self, name):
        return self.cmd(['ps', '-q', name])

    @property
    def services(self):
        out = self.cmd(['ps', '--services']).decode().splitlines()
        return [a.strip() for a in out]

    def restart(self):
        self.stop()
        self.start()
