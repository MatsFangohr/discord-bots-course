import datetime

jetzt = datetime.datetime.now()
andere_zeit = (
    jetzt
    + datetime.timedelta(seconds=647, minutes=34)
    - datetime.timedelta(days=365 * 7)
)

print(andere_zeit.strftime("%Y-%M-%d %H-%M-%S"))
