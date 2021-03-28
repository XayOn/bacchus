import os
from pathlib import Path

from bacchus.arr import Radarr, Lidarr, Sonarr
from bacchus.nextcloud import NextCloud
from bacchus.jackett import Jackett
from bacchus.transmission import Transmission
from bacchus.jellyfin import Jellyfin

__all__ = [Jackett, Transmission, Lidarr, Radarr, Sonarr, Jellyfin, NextCloud]


def main():
    for provider in __all__:
        getattr(provider(os.getenv('host')),
                'setup_{os.getenv("step")}_step')()
    Path('/data/bacchus_install_{os.getenv("step")}').write_text('')
