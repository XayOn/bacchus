from .base import HomeServerApp
from .base import DOCKER_PATH

from pathlib import Path
import os
import subprocess
import uuid


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
    PGID={os.getegid()}""")
        (DOCKER_PATH /
         '.env_nextcloud').write_text(f"""NEXTCLOUD_ADMIN_USER=admin
    NEXTCLOUD_ADMIN_PASSWORD={nextcloud_passwd}
    NEXTCLOUD_UPDATE=1
    """)

    def start(self):
        """Start."""
        subprocess.check_output('docker-compose',
                                'up',
                                'd',
                                cwd=DOCKER_PATH,
                                env=self.env)

    def stop(self):
        """Stop."""
        subprocess.check_output('docker-compose',
                                'stop',
                                cwd=DOCKER_PATH,
                                env=self.env)
