import os
import multiprocessing
from pathlib import Path

from bacchus.arr import Arr
from bacchus.jackett import Jackett
from bacchus.matrix import Matrix
from bacchus.transmission import Transmission
from bacchus.jellyfin import Jellyfin
from bacchus.organizr import Organizr

__all__ = [
    Jackett, Transmission, Arr, Jellyfin, Matrix, Organizr
]


def setup(provider):
    try:
        print(f"Setting up {provider.__class__.__name__}_{os.getenv('step')}")
        return getattr(provider(os.getenv('host')),
                       f'setup_{os.getenv("step")}_step')()
    except Exception as err:
        print(f"Could not configure {provider}: {err}")
        raise


def main():
    for provider in __all__:
        pro = multiprocessing.Process(target=setup, args=(provider, ))
        pro.start()
        pro.join(10)
        if pro.is_alive():
            pro.terminate()
            pro.join()
    Path(f'/data/bacchus_install_{os.getenv("step")}').write_text('')
