import time

# exists only as an example file for alternative_import.ipynb

wert = 7


def berechnung():
    time.sleep(time.time() % 2)
    return round(time.time() * 100) % 7
