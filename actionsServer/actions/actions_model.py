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
from .models import gptBackground, gptDefaultStory
# from .db import getKN
import json
import os


def send(d: CollectingDispatcher, obj: Any): d.utter_message(str(obj))
def getSlot_StoryStage(t: Tracker): return t.get_slot('story_stage')
def getUserLatestMEG(t: Tracker): return t.latest_message
def getUserText(t: Tracker): return getUserLatestMEG(t)["text"]

class ActionAskGptAnalysisStory(Action):

    def name(self) -> Text:
        return "action_ask_gpt_analysis_story"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        userText: str = getUserText(tracker)
        #result, rqBody = callGPT_AnswerQuestion(examples, userText)
        dispatcher.utter_message(text="CALL CUSTOM ACTION `action_ask_gpt_analysis_story`")
        #if os.environ.get("ActionServerMode", None) == "debug":
        #    dispatcher.utter_message(text=str(rqBody))

        # stage = getSlot_Stage(tracker)
        return []
        # return [
        #     SlotSet("stage", "CustomAction")
        # ]


class ActionAskGptExtendStory(Action):
    def name(self) -> Text:
        return "action_ask_gpt_extend_story"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="CALL CUSTOM ACTION `action_ask_gpt_extend_story`")
        dispatcher.utter_message(text="遊戲開始:\n`"+ gptBackground + gptDefaultStory)
        dispatcher.utter_message(text="user_text: `" + getUserText(tracker)+"`")
        dispatcher.utter_message(text="user sender_id: `"+tracker.sender_id+"`")
        


        if getUserText(tracker) == "NEXT":

            dispatcher.utter_message(text="遊戲將要結束 進行分析")
            return [
                SlotSet("story_started", False),
                SlotSet("story_finished", True)
            ]
        else:
            return []
