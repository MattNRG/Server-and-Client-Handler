import time
from wifi import connect

while True:
    try:
        connect()

    except Exception as r:
        print(f"{r}; retrying..")
        time.sleep(2)
