import os
import multiprocessing
from pathlib import Path

from bacchus.arr import Arr
from bacchus.matrix import Matrix
from bacchus.transmission import Transmission
from bacchus.jellyfin import Jellyfin

from loguru import logger

__all__ = [Transmission, Arr, Jellyfin, Matrix]


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
    """Setup configurations."""
    for provider in __all__:
        pro = multiprocessing.Process(target=setup, args=(provider, ))
        pro.start()
        pro.join(60)
        if pro.is_alive():
            pro.terminate()
            pro.join()
    step_path.write_text('')
