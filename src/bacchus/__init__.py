import os

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
