from typing import List, Dict, Any

class Stage:
    def __init__(self, _dict):
        # TODO: Check `_dict` is valid 
        self.__dict__.update(_dict)
    
    def __str__(self):
        return str(self.__dict__)



class MemoryLabel:
    def __init__(self, _dict=None):
        if _dict is not None:
            self.__dict__.update(_dict)
        else:
            self.__dict__.update({})

class StageLabel:
    def __init__(self, _dict=None):
        if _dict is not None:
            self.__dict__.update(_dict)
        else:
            self.__dict__.update({})



       
stage_intro_bot = Stage({
    "system": "reply/ans",
    "situation": {
        'role': """
            
            """,
		'task': "你身為前導機器人會提供使用者來問答。此外你並沒有其他的身分。",
    },
    "target": {
        
        'rag': [
            ["Hi", "哈囉，我是論證活動前導機器人，可以幫助學生透過問答來了解更多知識"],
            ["你是誰","我是一個由人工智慧技術建構的語言模製的論證活動前導機器人，可以幫助學生來了解論證活動。\n沒有問題的話，接下去會開始引導流程。"],
            ["這是什麼活動","這是一個論證活動，主題是台灣適不適合發展核能發電。"],
            ["怎樣才能參加這個活動","這是一個不定時的論證活動，詳情請洽中央網學所 吳研究室。"],

        ],
    },
    "action": {
        'toAgent': ["我是論證活動前導機器人，可以幫助學生透過問答來了解更多知識，有什麼想問我嗎" ],
        'continuer': "有關於我的任何問題嗎？ 如果沒有請說繼續",
        'opener': """
        Hi,您好。歡迎使用論證活動前導機器人，我是一個由人工智慧技術建構的論證活動前導機器人，
        目標是提供學生在進行論證前掌握一些基本的論證與核能發電的知識。
        同時也可以回應該活動的一些基本資訊。
        """
    }
})



def getStage(StageType: str) -> Stage:

    if StageType == "intro_bot":
        return stage_intro_bot

    raise RuntimeError("Non-defined Stage")