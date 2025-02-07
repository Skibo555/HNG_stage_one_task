import requests
import time

while True:
    requests.get("https://hng-stage-one-task-m9j7.onrender.com/api/classify-number")
    for i in range(0, 100000):
        time.sleep(120)
        print(f"Done request number {i}")
