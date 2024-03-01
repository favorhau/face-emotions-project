
# -*- coding: utf-8 -*-
import sqlite3
from log import log 

def sql_executor(func):
    def wrapper(__sql: str, __parameters: dict):
        query = " WHERE 1=1"
        for i, _ in __parameters.items():
            if(_):
                query += " AND report.{} = :{}".format(i, i)

        return func.execute(__sql + query, __parameters)
        
    return wrapper

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
