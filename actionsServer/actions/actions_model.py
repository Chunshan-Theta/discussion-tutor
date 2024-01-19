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
    return result
def send(d: CollectingDispatcher, obj: Any): d.utter_message(str(obj))
def getSlot_StoryStage(t: Tracker): return t.get_slot('story_stage')
def getUserLatestMEG(t: Tracker): return t.latest_message
def getUserText(t: Tracker): return getUserLatestMEG(t)["text"]
def getUserId(t: Tracker): return decrypt(t.sender_id)
client = createClient()
assert(checkClient(client))

def goNext(userId: str) -> List[str]:
    reply: List[str] = []
    REDISLABELSTATUS = userId
    userStatus = getByKey(client,REDISLABELSTATUS)

    ##
    if userStatus['stage'] == "intro_bot":
        reply.append("***intro_bot -> stage_discussion_tutor")
        stage = stage_discussion_tutor
        userStatus['stage'] = "stage_discussion_tutor"

    else:
        reply.append("[500] Action Stage Error")

    reply.append(stage.action["opener"])
    if "continuer" in stage.action:
        reply.append(stage.action["continuer"])

    updateDocuments(client, [{"key":REDISLABELSTATUS, "value": userStatus}])
    return reply   



class ActionAskGpt(Action):
    def name(self) -> Text:
        return "action_ActionAskGpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        REDISLABELSTATUS = getUserId(tracker)
        REDISLABELCOUNT = getUserId(tracker)+"-ROUNDCOUNT"
        dispatcher.utter_message("getUserId: "+getUserId(tracker))
        
        userStatus = getByKey(client, REDISLABELSTATUS)
        userStatus = userStatus if userStatus is NOT None else {}
        
        roundCount = getByKey(client, REDISLABELCOUNT)
        roundCount = roundCount if roundCount is not None else 0
            
        if "stage" not in userStatus:
            userStatus['stage'] = "stage_discussion_tutor"
            # dispatcher.utter_message("***ActionAskGpt")

        ##            
        for line in callGPTByStage(getUserId(tracker), userStatus['stage'], getUserText(tracker)).split("\n"):
            dispatcher.utter_message(line)

        if roundCount > 3:
            if userStatus['stage'] = "stage_discussion_tutor":
                replies = goNext(getUserId(tracker))
                for r in replies:
                    dispatcher.utter_message(r)
        ##
        updateDocuments(client, [{"key":REDISLABELSTATUS, "value": userStatus}])
        updateDocuments(client, [{"key":REDISLABELCOUNT, "value": roundCount}])

        return []




