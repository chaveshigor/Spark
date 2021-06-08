from datetime import datetime
import time

before = datetime.now()
#print(before)

while True:
    time.sleep(1)
    now = datetime.now()

    if (now - before).total_seconds() >= 10:
        break


print((now-before).total_seconds())
