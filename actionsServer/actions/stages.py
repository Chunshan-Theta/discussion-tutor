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


memoryTags = MemoryLabel({
    "historyOfTag": "historyOfTag"
})

       
stage_intro_bot = Stage({
    "system": {
            'id': "stage_intro_bot",
            'type': "interactive"
        },
    "situation": {
        'role': "Please provide an informative response to the user's question in a manner akin to that of a knowledgeable teacher. If uncertain or lacking confidence in the answer, it's acceptable to respectfully decline rather than provide inaccurate information. "
    },
    "target": {
        'rag': [
            ["Hi", "哈囉，我是課程前導機器人，可以幫助學生來了解論證活動，有什麼想問我嗎"],
            ["你是誰","我是一個由人工智慧技術建構的語言模製的課程前導機器人，可以幫助學生來了解論證活動。\n沒有問題的話，接下去會開始引導流程。"],
        ],
    },
    "action": {
        'toAgent': ["哈囉，我是課程前導機器人，有什麼想問我嗎" ]
    }
})
