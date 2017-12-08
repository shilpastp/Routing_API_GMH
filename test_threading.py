import datetime
import threading


def work():
    t = threading.Timer(60, work)
    t.start()
    print("stackoverflow")
    print(datetime.date.today())
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('now...', now)
    if now >= '2017-12-06 02:04:00':
        t.cancel()


work()
