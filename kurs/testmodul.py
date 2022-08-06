pi = 3.14159265358979323846


def fakultaet(zahl):
    ergebnis = 1
    for i in range(1, zahl + 1):
        ergebnis = ergebnis * i
    return ergebnis


def magie(zahl):
    return fakultaet(int(8 * zahl / 2 % 9))


print("Diese Nachricht kannst du erstmal ignorieren.")
