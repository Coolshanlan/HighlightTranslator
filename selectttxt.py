import datetime
import time

a = datetime.datetime.now()
time.sleep(1)
b = datetime.datetime.now()
print((b-a).seconds)
print((b-a).microseconds)
print((b-a))
print((b-a).total_seconds())
print((b-a).seconds*1000 + (b-a).microseconds)
