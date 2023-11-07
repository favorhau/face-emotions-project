import sqlite3
import os
from log import log

# 连接数据库，如果不存在数据库则自动创建
db_file = os.path.join(os.path.dirname(__file__), 'db.sqlite')
db = sqlite3.connect(db_file)

# 创建游标
cursor = db.cursor()


# 初始化数据库
def init():

    __exists__ = cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = '__exists__';
    """).fetchone()
    
    if(__exists__):
        log('', '数据库已初始化')
    else:
        try:
        
            cursor.execute('create table __exists__ (id INTEGER PRIMARY KEY)')
            cursor.execute('create table user (id varchar(20) primary key, name varchar(20), fre int)')
            cursor.execute('create table report (id varchar(20) primary key, user_id varchar(20), date varchar(20), fre int)')
            log('', '数据库初始化成功')
        except Exception as e:
            log(str(e), '数据库初始化失败')


if __name__ == '__main__':
    # init()
    pass
    # print(cursor)
