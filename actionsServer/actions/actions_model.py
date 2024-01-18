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

def goNext(userId: str) -> List[Dict[Text, Any]]:
    reply: List[str] = []
    userStatus = getByKey(client,userId)
    if userStatus is None:
        userStatus = {}
    if "stage" not in userStatus:
        userStatus['stage'] = "intro_bot"

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

    updateDocuments(client, [{"key":userId, "value": userStatus}])
    return []    



class ActionAskGpt(Action):
    def name(self) -> Text:
        return "action_ActionAskGpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message("getUserId: "+getUserId(tracker))
        userStatus = getByKey(client,getUserId(tracker))
        if userStatus is None:
            userStatus = {}
            
        if "stage" not in userStatus:
            userStatus['stage'] = "intro_bot"
            # dispatcher.utter_message("***ActionAskGpt")
            dispatcher.utter_message(stage_intro_bot.action["opener"])

        ##            
        for line in callGPTByStage(getUserId(tracker), userStatus['stage'], getUserText(tracker)).split("\n"):
            dispatcher.utter_message(line)
        updateDocuments(client, [{"key":getUserId(tracker), "value": userStatus}])
        return []




