# -*- coding: utf-8 -*-
import sqlite3
import os
from log import log

# 连接数据库，如果不存在数据库则自动创建
db_file = os.path.join(os.path.dirname(__file__), 'db.sqlite')
db = sqlite3.connect(db_file)

# 创建游标
cursor = db.cursor()


# 初始化数据库
def init(mock: bool = True):

    __exists__ = cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = '__exists__';
    """).fetchone()
    
    if(__exists__):
        log('', '数据库已初始化')
    else:
        try:
        
            # 创建是否存在表
            cursor.execute('create table IF NOT EXISTS __exists__ (id INTEGER PRIMARY KEY)')
            # 用户表
            cursor.execute('create table IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(20), startTime varchar(20), endTime varchar(20))')
            # 原始数据表
            cursor.execute('create table IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id varchar(20), emotion varchar(20), date varchar(20))')
            # 报告表
            cursor.execute('create table IF NOT EXISTS report (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id varchar(20), day varchar(20), type varchar(10), title varchar(20), data TEXT)')


            if(mock):
                # 如果选择模拟数据，则添加数据
                user_data = [
                    ('戴景昊', '00:00:00', '23:59:59'),
                    ('阿拉风', '08:00:00', '23:59:59'),
                ]
                for data in user_data:
                    cursor.execute("INSERT INTO user (name, startTime, endTime) VALUES (?, ?, ?)", data)

                db.commit()
            log('', '数据库初始化成功')
        except Exception as e:
            try:
                cursor.execute('DROP TABLE __exists__')
                cursor.execute('DROP TABLE user')
                cursor.execute('DROP TABLE data')
                cursor.execute('DROP TABLE report')
            except Exception: pass
            log(str(e), '数据库初始化失败')
            
        db.close()


if __name__ == '__main__':
    # init()
    pass
    # print(cursor)
