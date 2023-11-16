# -*- coding: utf-8 -*-
from db.utils import handle_database_exceptions
from datetime import datetime
from . import db_file
import sqlite3

@handle_database_exceptions
def get_users(date_filter: tuple = None):
    """
    获取用户
    @params dete_filter 日期筛选 eg: (time(0,1,0) 代表 00:01:00, datetime(11,16,0) 代表 11:16:00)

    ```python
    from datetime import time
    res = get_users(cursor, time(0, 1, 0), time(12,0,0))
    ```
    """
    # 因为多线程执行，每一次需要单独连接数据库
    db = sqlite3.connect(db_file)
    cursor = db.cursor()

    if date_filter:
        current_date = datetime.now().date()
        start_time, end_time = date_filter
        start_datetime = datetime.combine(current_date, start_time).strftime('%H:%M:%S')
        end_datetime = datetime.combine(current_date, end_time).strftime('%H:%M:%S')
        cursor.execute("SELECT * FROM user WHERE startTime <= ? AND endTime >= ?", (start_datetime, end_datetime))
    else:
        cursor.execute("SELECT * FROM user")
        
    result = cursor.fetchall()
    
    db.close()
    return result
     