# -*- coding: utf-8 -*-
import sqlite3
from db.utils import handle_database_exceptions
from datetime import datetime
from . import db_file

@handle_database_exceptions
def insert_data(user_id: str, emotion: str):
    """
    插入数据
    @params user_id 用户id
    @params emotion 监测到的情绪
    """
    # 因为多线程执行，每一次需要单独连接数据库
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO data (user_id, emotion, date) VALUES (?, ?, ?)", (user_id, emotion, current_date))

    result = cursor.lastrowid
    
    db.commit()
    db.close()
    return result
     
@handle_database_exceptions
def fetch_data(user_id: str, day: str):
    """
    获取数据
    @params user_id 用户id
    @params day 数据的日期 精确到日 %Y-%m-%d
    """
    
     # 因为多线程执行，每一次需要单独连接数据库
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute("SELECT emotion FROM data WHERE strftime('%Y-%m-%d', date) = ? and user_id = ?", (day, user_id))

    result = cursor.fetchall()

    return result