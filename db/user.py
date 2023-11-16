# -*- coding: utf-8 -*-

import sqlite3

from log import log
from . import cursor
from datetime import datetime, time

def handle_database_exceptions(func):
    """
    装饰器，用于统一拦截数据库错误的异常
    """
    def wrapper(*args, **kwargs):
        try:
            # 执行被装饰的函数
            result = func(*args, **kwargs)
            return result
        except sqlite3.Error as e:
            # 捕获 SQLite 数据库异常
            log(f"SQLite Database Error: {e}")
            # 在这里可以添加更多的处理逻辑，如记录日志、发送通知等
            return None  # 或者根据需要返回其他默认值
        except Exception as e:
            # 捕获其他异常
            log(f"Unexpected Error: {e}")
            # 在这里可以添加更多的处理逻辑，如记录日志、发送通知等
            return None  # 或者根据需要返回其他默认值

    return wrapper

@handle_database_exceptions
def get_users(date_filter: tuple = None):
    """
    获取用户
    @params dete_filter 日期筛选 eg: (time(0,1,0) 代表 00:01:00, datetime(11,16,0) 代表 11:16:00)

    ```python
    from datetime import time
    res = get_users(time(0, 1, 0), time(12,0,0))
    ```
    """
    if date_filter:
        current_date = datetime.now().date()
        start_time, end_time = date_filter
        start_datetime = datetime.combine(current_date, start_time).strftime('%H:%M:%S')
        end_datetime = datetime.combine(current_date, end_time).strftime('%H:%M:%S')

        cursor.execute("SELECT * FROM user WHERE startTime >= ? AND endTime <= ?", (start_datetime, end_datetime))
    else:
        cursor.execute("SELECT * FROM user")
        
    result = cursor.fetchall()
    
    return result
     