from typing import Counter
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
    
    # 快乐指数
    prousal = (0*emotions_counter['surprise']+(-2)*emotions_counter['fear']+(-3)*emotions_counter['angry']+(-4)*emotions_counter['disgust']+
           4*emotions_counter['happy']+0*emotions_counter['neutral']+(-4)*emotions_counter['sad']) / sum(emotions_counter.values()) * 100

    # 悲伤指数
    arousal = (5*emotions_counter['surprise']+3*emotions_counter['fear']+2*emotions_counter['angry']+1*emotions_counter['disgust']+
           1*emotions_counter['happy']+(-1)*emotions_counter['neutral']+(-1)*emotions_counter['sad']) / sum(emotions_counter.values()) * 100
    
    rader_data = [
        { "name": '关怀', "value": 0.71*prousal+0.12*arousal, },
        { "name": '戒备', "value":  -0.24*prousal, },
        { "name": '同理心', "value": 0.23*prousal+0.59*arousal, },
        { "name": '恐慌', "value": -0.26*prousal+0.37*arousal, },
        { "name": '自杀倾向', "value": 0.48*arousal, },
        { "name": '情绪稳定', "value": 0.37*prousal-0.44*arousal, },
        { "name": '社交期望', "value": 0.35*prousal-0.20*arousal, },
        { "name": '躁动', "value": -0.26*prousal+0.22*arousal, },
        { "name": '药物使用', "value": 0.33*arousal, },
    ]
        
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
            "prousal": prousal,
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
    
    return