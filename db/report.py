# -*- coding: utf-8 -*-

from . import db_file
from db.utils import handle_database_exceptions
import sqlite3

@handle_database_exceptions
def insert_report(user_id: str, day: str, type: str, title: str, data: str):
    """
    插入报告
    @params user_id 用户id
    @params day 当前日期
    @params type 类型 饼图pie 柱状图
    @params title 标题
    @params data Object Str [{"name" : "", "value": 10}] //图数据 json.loads(data) = objectData
    """
    # 因为多线程执行，每一次需要单独连接数据库
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    cursor.execute("INSERT INTO report (user_id, day, type, title, data) VALUES (?, ?, ?, ?, ?)", (user_id, day, type, title, data))

    result = cursor.lastrowid
    
    db.commit()
    db.close()
    return result