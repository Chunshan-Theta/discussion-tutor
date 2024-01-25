# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .models import *
import json
import os
from .document import *
from .stages import *
import base64

def decrypt(decoded_text):
    SecretKey = "20240116";
    decoded_text = base64.b64decode(decoded_text).decode('utf-8')
    result = ''
    for i in range(len(decoded_text)):
        charCode = ord(decoded_text[i]) ^ ord(SecretKey[i % len(SecretKey)])
        result += chr(charCode)
    assert len(result.split("."))==4
    return result
def send(d: CollectingDispatcher, obj: Any): d.utter_message(str(obj))
def getSlot_StoryStage(t: Tracker): return t.get_slot('story_stage')
def getUserLatestMEG(t: Tracker): return t.latest_message
def getUserText(t: Tracker): return getUserLatestMEG(t)["text"]
def getUserId(t: Tracker): return decrypt(t.sender_id)
client = createClient()
assert(checkClient(client))

def goNext(userStatus: Dict[str, Any],redisLabel_status) -> List[str]:
    reply: List[str] = []
    #reply.append("***goNext: userStatus -> "+ str(userStatus))


    ##
    if userStatus['stage'] == "stage_discussion_tutor":
        #reply.append("***stage_discussion_tutor -> stage_rubric_tutor")
        stage = stage_rubric_tutor
        userStatus['stage'] = "stage_rubric_tutor"
        updateDocuments(client, [{"key":redisLabel_status, "value": userStatus}])

    else:
        reply.append("[500] Action Stage Error")

    reply.append(stage.action["opener"])
    if "continuer" in stage.action:
        reply.append(stage.action["continuer"])

    
    return reply   



class ActionAskGpt(Action):
    def name(self) -> Text:
        return "action_ActionAskGpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        REDISLABELSTATUS = getUserId(tracker)
        REDISLABELCOUNT = getUserId(tracker)+"-ROUNDCOUNT"
        
        userStatus = getByKey(client, REDISLABELSTATUS)
        userStatus = userStatus if userStatus is not None else {}
        
        roundCount = getByKey(client, REDISLABELCOUNT)
        roundCount = roundCount if roundCount is not None else 1

        #dispatcher.utter_message("***ActionAskGpt: REDISLABELSTATUS: "+REDISLABELSTATUS)
        #dispatcher.utter_message("***ActionAskGpt: REDISLABELCOUNT: "+REDISLABELCOUNT)
            
        # the first round
        if "stage" not in userStatus:
            userStatus['stage'] = "stage_discussion_tutor"
            # dispatcher.utter_message("***ActionAskGpt")
        

        ##
        ## TODO: DONT DO AGAING ANALYSIS           
        for line in callGPTByStage(getUserId(tracker), userStatus['stage'], getUserText(tracker)).split("\n"):
            dispatcher.utter_message(line)

        #dispatcher.utter_message("***roundCount: "+str(roundCount))
        if roundCount > 3:
            if userStatus['stage'] == "stage_discussion_tutor":
                replies = goNext(userStatus,REDISLABELSTATUS)
                for r in replies:
                    dispatcher.utter_message(r)
                    
                    
        ##
        updateDocuments(client, [{"key":REDISLABELCOUNT, "value": roundCount+1}])

        return []




