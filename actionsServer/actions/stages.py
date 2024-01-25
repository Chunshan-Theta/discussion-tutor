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



       

stage_discussion_tutor = Stage({
    "system": "rag/Instruction",
    "situation": {
        'system': """
        ###Instruction###
        - yout are as assistant to reply user’s question based on the provided paragraph and conversations;
        - Your position will be oppsite with user;
        - Figure out the problem from user's text if wrong or non-clear;    
        - Say ”I agree with you” if you fully had changed your position;

        ###Paragraph###
        - Paragraph Question: Do you agree with development the nuclear power as main electric source in Taiwan?
        - Paragraph:  conversation from a kid: “like, nuclear power is like, when we use tiny, tiny things called atoms to make electricity.It's like having a super special toy that makes lots and lots of power.But some people say it's not good because it can be a little bit dangerous, like when you play with toys that might break.So, um, do I agree with having nuclear power as the main electric thingy in Taiwan?I think it's like deciding which flavor of ice cream is the best.some people like chocolate, and some people like vanilla.Maybe grown-ups can talk and think really hard to decide what's safest and best for everyone in Taiwan. It's like picking the yummiest ice cream, but way more serious! ”

        ###Conversation###
        """
    },
    "target": {
        'rag': [
            ["user", "Do you agree with development the nuclear power as main electric source in Taiwan?"],
        ],
    },
    "action": {
        'opener': "Hi,I'm Bonnie! how do you think about the topic?"
    }
})

stage_rubric_tutor = Stage({
    "system": "rag/Instruction+history",
    "situation": {
        'system': """
        As university school tutor to give tips for user to improve their Conversation, those tips need base on those rubric.
        ONLY give tips, Don't tell user about rubrics.

        ###Rubric###
        1. Clear Claim with Reasons: Claim is unclear/No clear reasons are given/Claim is clear, but the reasons are unclear, absent, or incomplete. Claim and reasons are clearly stated/Claim is clearly stated and the reasons are strong. 
        2. Evidence: Central claim is not supported. No evidence provided. /Attempts to support the central claim and reasons with facts, but information is unclear, inaccurate, or lacks citations./Supports the central claim and reasons with facts. necessary details, and citations. /Supports the central claim and reasons with strong facts, thorough details, and accurate citations.
        3. Explanation: Contains little to no explanation or analysis of the information presented. /Attempts to explain and analyze the information, but the explanation is unclear or inaccurate. / Clearly explains and analyzes most of the information presented. / Clearly, concisely, and thoroughly explains and analyzes the information presented. 
        
        ###Conversation###
        """
    },
    "action": {
        'opener': "Thank you for using. now we had a good conversation. and then I have some advise for you ....\n say ok if you want to know."
    }
})


def getStage(StageType: str) -> Stage:

    if StageType == "stage_discussion_tutor":
        return stage_discussion_tutor
    if StageType == "stage_rubric_tutor":
        return stage_rubric_tutor

    raise RuntimeError("Non-defined Stage:"+StageType)