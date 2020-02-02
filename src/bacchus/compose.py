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
        return {'COMPOSE_PROJECT_NAME': self.meta['project_name']}

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
        shutil.copyfile((TEMPLATES / 'docker-compose.yml').as_posix(),
                        (DOCKER_PATH / 'docker-compose.yml').as_posix())

        # Hack to allow nginx docker config mount
        nginx_path = DOCKER_PATH / 'data' / 'nginx'
        nginx_path.mkdir(exist_ok=True, parents=True)
        (nginx_path / 'nginx.conf').write_text('')

    def start(self):
        """Start."""
        print(f'starting {self.meta["project_name"]}')
        subprocess.check_output(
            ['docker-compose', '-p', self.meta['project_name'], 'up', '-d' ],
            cwd=DOCKER_PATH,
            env=self.env)

    def stop(self):
        """Stop."""
        subprocess.check_output(['docker-compose', 'stop'],
                                cwd=DOCKER_PATH,
                                env=self.env)

    def restart(self):
        self.stop()
        self.start()
