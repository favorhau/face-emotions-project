# 规范打印 log
from datetime import datetime

def log(error, *args):
    date_format = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('[{}]'.format(date_format), *args , '[原因]' if error else '', error)