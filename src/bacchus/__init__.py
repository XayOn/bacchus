import os
import multiprocessing
import logging
from pathlib import Path

from bacchus.arr import Arr
from bacchus.jackett import Jackett
from bacchus.matrix import Matrix
from bacchus.transmission import Transmission
from bacchus.jellyfin import Jellyfin
from bacchus.organizr import Organizr

from loguru import logger

__all__ = [Jackett, Transmission, Arr, Jellyfin, Matrix, Organizr]


def setup(provider):
    """Setup a provider with some environment variables"""
    try:
        logger.info(f"Setting up {provider.__name__}_{os.getenv('step')}")
        return getattr(provider(os.getenv('host')),
                       f'setup_{os.getenv("step", "first")}_step')()
    except Exception as err:
        logger.exception(f"Could not configure {provider}: {err}")
        raise


def main():
    """Wait 60 seconds for each provider to finish.

    Should not take that long! Terminate otherwise
    Parallelize providers configuration
    """
    step_path = Path(f'/data/bacchus_install_{os.getenv("step", "first")}')
    if step_path.exists():
        logger.info(
            'Already executed. Deleted installfile if you want to reinstall')
        return
    for provider in __all__:
        pro = multiprocessing.Process(target=setup, args=(provider, ))
        pro.start()
        pro.join(60)
        if pro.is_alive():
            pro.terminate()
            pro.join()
    step_path.write_text('')
