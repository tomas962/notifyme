import threading
import multiprocessing
import time

threads = []

t1 = time.time()
for i in range(10000):
    t = threading.Thread(target=lambda: i > 1)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

t2 = time.time()

print("ELAPSED TIME:")
print(t2-t1)
