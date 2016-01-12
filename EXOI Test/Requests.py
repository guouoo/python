import datetime
def givetime():
    time  = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return time
