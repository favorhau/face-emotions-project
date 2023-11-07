# -*- coding: utf-8 -*-
import db
from api import app


if __name__ == '__main__':
    # 初始化数据库 若不存在数据库则自动新建
    db.init()
    # 开启 web 服务
    app.run('0.0.0.0', port=8080)