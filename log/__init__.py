# -*- coding: utf-8 -*-
# 规范打印 log
from datetime import datetime

MAX_LENGTH = 10

def log(error, *args):
    date_format = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open('./log/log', 'r') as f:
            data = f.read().splitlines()
            current_err_line = ' '.join(['[{}]'.format(date_format), *args , '[原因]' if error else '', error])
            if(len(data) >= MAX_LENGTH):
                new_data = '\n'.join([*data[len(data)-MAX_LENGTH + 1:len(data) + 1], current_err_line])
            else:
                new_data = '\n'.join([*data, current_err_line])
        f.close()
        
        with open('./log/log', "w") as f:
            f.write(new_data)

        f.close()
    except Exception as e:
        print('写入日志失败', str(e))
    print('[{}]'.format(date_format), *args , '[原因]' if error else '', error)