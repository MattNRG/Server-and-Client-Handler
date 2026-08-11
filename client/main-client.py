import time
from wifi import connect, connected

while True:
    try:
        connect()

    except Exception as r:
        connected = False
        print(f"{r}; retrying..")
        time.sleep(2)
