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

def send(d: CollectingDispatcher, obj: Any): d.utter_message(str(obj))
def getSlot_StoryStage(t: Tracker): return t.get_slot('story_stage')
def getUserLatestMEG(t: Tracker): return t.latest_message
def getUserText(t: Tracker): return getUserLatestMEG(t)["text"]
def getUserId(t: Tracker): return t.sender_id
client = createClient()
assert(checkClient(client))




class ActionAskGpt(Action):
    def name(self) -> Text:
        return "action_ActionAskGpt"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userStatus = getByKey(client,getUserId(tracker))
        if userStatus is None:
            userStatus = {}
        if "stage" not in userStatus:
            userStatus['stage'] = "intro_bot"
            # dispatcher.utter_message("***ActionAskGpt")
            dispatcher.utter_message(stage_intro_bot.action["opener"])

        ##
        if userStatus['stage'] == "intro_bot":
            # dispatcher.utter_message("***intro_bot")
            pass
        elif userStatus['stage'] == "intro_unclear_power":
            # dispatcher.utter_message("***intro_unclear_power")
            pass
        elif userStatus['stage'] == "intro_discussion":
            # dispatcher.utter_message("***intro_discussion")
            pass

        elif userStatus['stage'] == "intro_ask":
            # dispatcher.utter_message("***intro_ask")
            pass

        elif userStatus['stage'] == "intro_reply":
            # dispatcher.utter_message("***intro_reply")
            pass

        elif userStatus['stage'] == "finish":
            # dispatcher.utter_message("***finish")
            return []
        else:
            dispatcher.utter_message("[500] Action Stage Error")
            return []

            
        for line in callGPTByStage(getUserId(tracker), userStatus['stage'], getUserText(tracker)).split("\n"):
            dispatcher.utter_message(line)       
        updateDocuments(client, [{"key":getUserId(tracker), "value": userStatus}])
        return []


class ActionGoNext(Action):
    def name(self) -> Text:
        return "action_ActionGoNext"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userStatus = getByKey(client,getUserId(tracker))
        if userStatus is None:
            userStatus = {}
        if "stage" not in userStatus:
            userStatus['stage'] = "intro_bot"

        ##
        if userStatus['stage'] == "intro_bot":
            dispatcher.utter_message("***intro_bot -> intro_unclear_power")
            dispatcher.utter_message(stage_intro_unclear_power.action["opener"])
            userStatus['stage'] = "intro_unclear_power"

        elif userStatus['stage'] == "intro_unclear_power":
            dispatcher.utter_message("***intro_unclear_power -> intro_discussion")
            dispatcher.utter_message(stage_intro_discussion.action["opener"])
            userStatus['stage'] = "intro_discussion"
            

        elif userStatus['stage'] == "intro_discussion":
            dispatcher.utter_message("***intro_discussion -> intro_ask")
            dispatcher.utter_message(stage_try_ask.action["opener"])
            userStatus['stage'] = "intro_ask"

        elif userStatus['stage'] == "intro_ask":
            dispatcher.utter_message("***intro_ask -> intro_reply")
            dispatcher.utter_message(stage_try_reply.action["opener"])
            userStatus['stage'] = "intro_reply"

        elif userStatus['stage'] == "intro_reply":
            dispatcher.utter_message("***intro_reply -> finish")
            userStatus['stage'] = "finish"

        elif userStatus['stage'] == "finish":
            dispatcher.utter_message("***Hi It's bot! finish")

        else:
            dispatcher.utter_message("[500] Action Stage Error")

        updateDocuments(client, [{"key":getUserId(tracker), "value": userStatus}])
        return []    
