import time
from typing import Callable


def laufzeit(func: Callable) -> float:
    start_zeit = time.time()
    func()
    return time.time() - start_zeit
