import time

start = time.time()

for i in range(101):  # 101 damit 100 noch dabei ist
    time.sleep(0.1)
    print(i / 10)

print(f"zeit: {time.time() - start}")

time.sleep(3)
print("alternative lösung:")

start = time.time()

zeit_gewartet = 0

for i in range(101):  # 101 damit 100 noch dabei ist
    time.sleep(0.1)
    zeit_gewartet += 0.1
    print(zeit_gewartet)

print(f"zeit: {time.time() - start}")
