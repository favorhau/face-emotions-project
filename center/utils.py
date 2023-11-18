from db.data import fetch_data


def cal_report(user_id: str, day):
    """
    根据初始的情绪 计算报告
    @params user_id 用户id
    @params day 数据的日期 精确到日 %Y-%m-%d
    """
    
    # [('neutral',), ('neutral',), ('neutral',), ('happy',), ('sad',), ('neutral',)]
    emotions = fetch_data(user_id=user_id, day=day)
    emotions_list = [_[0] for _ in emotions]
    
    # 计算 pie : 情感比例
    
    
    
    # 计算 pie : 情感分布
    
    
    # 计算 radar : 心理分析
    
    
    
    return