# -*- coding: utf-8 -*-

from . import db_file
from db.utils import handle_database_exceptions, sql_executor
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
    
    
@handle_database_exceptions
def fetch_report(user_id: str, id: int, name: str, type = 'fuzzy'):
    """
    获取报告
    @params user_id 用户id
    @params id 报告id
    @params name 用户姓名
    @params type 精准或模糊查询 'fuzzy' | 'term'
    """
    # 因为多线程执行，每一次需要单独连接数据库
    db = sqlite3.connect(db_file)
    cursor = db.cursor()
    
    if(type == 'term'):
       sql_executor(cursor)("SELECT report.*, user.name FROM report JOIN user ON report.user_id = user.id ", {
        "user_id": user_id, "id": id
       })
    #    cursor.execute("SELECT report.*, user.name FROM report JOIN user ON report.user_id = user.id WHERE (report.user_id = ? AND report.name = ? AND report.id = ?);", (user_id, name, id))
    else:
        if user_id:
            cursor.execute("SELECT report.*, user.name FROM report JOIN user ON report.user_id = user.id WHERE (report.user_id = ? OR report.id = ?);", (user_id, id, ))
        else:
            if name:
                cursor.execute('SELECT report.id, user.id, report.day, report.type, report.title, report.data, user.name FROM user JOIN report ON user.id = report.user_id WHERE user.name = "{}";'.format(name))
            else:
                cursor.execute("SELECT report.*, user.name FROM report JOIN user ON user.id = report.user_id;")
        
        
    result = cursor.fetchall()

    db.commit()
    db.close()
    return result