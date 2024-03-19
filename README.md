# Atom GO 面部表情识别分析系统

> 本程序适配开发版（JETSON-NANO-DEV-KIT）

## Overview

精度以1s为基准，查一次数据库

## Quick Start

1. 中心服务器运行 
```python
python main.py -s
```

2. 开发版/采集器 运行
```python
python main.py -c
```
## Dependencies

nodejs v16.15.0

```bash
    ENV=linux python3 main.py
```


## Structure

### db

sqlite 经测试 10w 条数据占据的磁盘空间 < 100M

## Enhancement

1. 中心服务器

- 2FA 授权管理员

- 报告查询加分页功能

- 生成当前报告按钮改良

- 美化/跨端


2. 算法层面

- 更精准的人脸识别算法

- 更精准的情绪识别

- 更 make sense 的情绪报告

## Pile line

1. match -> muti-face-id

2. clock -> database -> raw data

3. clock -> calculate -> object data

4. user -> front-end -> back-end


## Others

1. 边缘计算 -> 人脸识别 -> 服务器

- 如果想在开发版上做实时用户人脸识别 -> 不可行

- 多用户 30 有点困难

2. 多场景 / 单场景

3. timeline

- 完善的 system

- 把人脸识别 放在 服务器


