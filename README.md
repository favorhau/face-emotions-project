# Atom GO 面部表情识别分析系统

> 本程序适配开发版（JETSON-NANO-DEV-KIT）

## Overview

精度以1s为基准，查一次数据库

## Quick Start



## Dependencies

nodejs v16.15.0

```bash
    ENV=linux python3 main.py
```


## Structure

### db

sqlite 经测试 10w 条数据占据的磁盘空间 < 100M

## Enhancement


## Pile line

1. match -> muti-face-id

2. clock -> database -> raw data

3. clock -> calculate -> object data

4. user -> front-end -> back-end