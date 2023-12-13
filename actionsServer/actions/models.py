import requests
import json
from typing import List, Any, Dict
import os
from .document import *
from .stages import *

def callGpt(
        messages: List[Dict[str,str]],
        temperature: float = 0.3
    ) -> str:
    url: str = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": temperature,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "max_tokens": 800,
        "presence_penalty": 0,
        "frequency_penalty": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+ os.environ.get("ChatGPTApiKey", "None")
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        return str(response.json()['choices'][0]['message']['content'])
    except:
        return "OPEN API DOWN -> ERROR:"+str(response.text)


client = createClient()
assert(checkClient(client))

def setHistory(userId:str, memory: List[Any]):
    return updateDocuments(client,[{
            'key': userId+memoryTags.historyOfTag,
            'value': memory
        }],"$")
def getHistory(userId:str): return getByKey(client, userId + memoryTags.historyOfTag)

#
def callGPT_IntroBot(userId: str,userText: str) -> str:

    botReply: str = ""
    prompts = [{
        "role": "system",
        "content": stage_intro_bot.situation["role"]
    }]
    for unit in stage_intro_bot.target['rag']:
        prompts.append({
                    "role": "assistant",
                    "content": "\n".join(stage_intro_bot.action["both"])
                })
        prompts.append({
                    "role": "user",
                    "content": unit[0]
                })
        prompts.append({
                    "role": "assistant",
                    "content": unit[1]
                })
    prompts.append({
                    "role": "assistant",
                    "content": "\n".join(stage_intro_bot.action["both"])
                })
    prompts.append({
                    "role": "user",
                    "content": userText
                })
    botReply += "\n***".join([str(unit) for unit in prompts])
    botReply += "\n"+callGpt(prompts, 0.5)
    

    return botReply       


