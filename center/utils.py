# -*- coding: utf-8 -*-
from typing import Counter
from datetime import datetime, timedelta
from db.data import fetch_data
from db.report import insert_report
import json

def dumps_report(user_id: str, day: str):
    """
    根据初始的情绪 计算报告 并导出
    @params user_id 用户id
    @params day 数据的日期 精确到日 %Y-%m-%d
    """
    
    # [('neutral',), ('neutral',), ('neutral',), ('happy',), ('sad',), ('neutral',)]
    emotions = fetch_data(user_id=user_id, day=day)
    emotions_list = [_[0] for _ in emotions]
    emotions_counter = Counter(emotions_list)
    
    # 计算 pie : 情感比例
    
    """
    data = [{ value: 1048, name: 'Search Engine' },
        { value: 735, name: 'Direct' },]
    """
    pie1_data = [{"value": v, "name": k} for k, v in emotions_counter.items()]
    

    # 计算 pie : 情感分布
    pie2_transfer =  { 
        'active': ['surprise', 'fear', 'angry', 'disgust', 'happy'],
        'neutral': ['neutral'],
        'inacitive': ['sad'],
    }
    pie2_data = [
        {
            "value": sum([emotions_counter[_] for _ in v]),
            "name":  k
        } for k, v in pie2_transfer.items()
    ]
    
    # 计算 radar : 心理分析
    
    # 快乐程度
    pleasure = (0*emotions_counter['surprise']+(-2)*emotions_counter['fear']+(-3)*emotions_counter['angry']+(-4)*emotions_counter['disgust']+
           4*emotions_counter['happy']+0*emotions_counter['neutral']+(-4)*emotions_counter['sad']) / (sum(emotions_counter.values()) if sum(emotions_counter.values()) != 0 else 1) * 100

    # 活力程度
    arousal = (5*emotions_counter['surprise']+3*emotions_counter['fear']+2*emotions_counter['angry']+1*emotions_counter['disgust']+
           1*emotions_counter['happy']+(-1)*emotions_counter['neutral']+(-1)*emotions_counter['sad']) / (sum(emotions_counter.values()) if sum(emotions_counter.values()) != 0 else 1) * 100
    
    rader_data = [
        { "name": '关怀', "value": 0.71*pleasure+0.12*arousal, },
        { "name": '戒备', "value":  -0.24*pleasure, },
        { "name": '同理心', "value": 0.23*pleasure+0.59*arousal, },
        { "name": '恐慌', "value": -0.26*pleasure+0.37*arousal, },
        { "name": '自杀倾向', "value": 0.48*arousal, },
        { "name": '情绪稳定', "value": 0.37*pleasure-0.44*arousal, },
        { "name": '社交期望', "value": 0.35*pleasure-0.20*arousal, },
        { "name": '躁动', "value": -0.26*pleasure+0.22*arousal, },
        { "name": '药物使用', "value": 0.33*arousal, },
    ]
    
    # 计算 line : 心理走向
    
    # 分成10部分
    parts = 10

    def split_into_equal_parts(array, num_parts):
        # 计算每份的大小（向上取整，以确保每份都有至少一个元素）
        part_size = -(-len(array) // num_parts)

        # 使用列表解析进行分割
        divided_array = [array[i:i + part_size] for i in range(0, len(array), part_size)]

        return divided_array

    # emotions_split: [[('neutral', '2023-11-19 10:02:26')], [('neutral', '2023-11-19 10:02:27')], [('neutral', '2023-11-19 10:02:28')], [('angry', '2023-11-19 10:02:30')], [('neutral', '2023-11-19 10:02:31')], [('happy', '2023-11-19 10:02:32')], [('happy', '2023-11-19 10:02:33')], [('happy', '2023-11-19 10:02:34')], [('neutral', '2023-11-19 10:02:35')]]
    emotions_split = split_into_equal_parts([(_[0], _[1]) for _ in emotions], parts)
    
    line_data = {
        "pleasure": [],
        "arousal": [],
        'timeInterval': []
    }
    for part in emotions_split:
        c = Counter([_[0] for _ in part])
        timeInterval = part[0][1]
        
        pleasure = (0*c['surprise']+(-2)*c['fear']+(-3)*c['angry']+(-4)*c['disgust']+
           4*c['happy']+0*c['neutral']+(-4)*c['sad']) / (sum(c.values()) if sum(c.values()) != 0 else 1) * 100

        # 活力程度
        arousal = (5*c['surprise']+3*c['fear']+2*c['angry']+1*c['disgust']+
            1*c['happy']+(-1)*c['neutral']+(-1)*c['sad']) / (sum(c.values()) if sum(c.values()) != 0 else 1) * 100
        
        line_data['arousal'].append(arousal)
        line_data['pleasure'].append(pleasure)
        line_data['timeInterval'].append(timeInterval)
        
    insert_report(
        user_id=user_id,
        day=day,
        type='pie1',
        title='情感比例',
        data=json.dumps(pie1_data),
    )
    
    insert_report(
        user_id=user_id,
        day=day,
        type='pie2',
        title='情感分布',
        data=json.dumps(pie2_data),
    )
    
    insert_report(
        user_id=user_id,
        day=day,
        type='tread',
        title='活力指数',
        data=json.dumps({
            "pleasure": pleasure,
            "arousal": arousal,
        }),
    )
    
    insert_report(
        user_id=user_id,
        day=day,
        type='radar',
        title='心理分析',
        data=json.dumps(rader_data),
    )
    
    insert_report(
        user_id=user_id,
        day=day,
        type='line',
        title='心理走向',
        data=json.dumps(line_data),
    )
    
    return