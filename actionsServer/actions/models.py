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




#
def genSystemPrompt(stage: Stage):
    systemPrompt = stage.situation["role"]+stage.situation["task"]+"\n\nplease Reply base on you know.\n you know:\n"
    for unit in stage.target['rag']:
        systemPrompt += "- "+unit[0]+"?"+unit[1]
        systemPrompt += "\n"
    return systemPrompt+"\n keep reply simply with english"


def callGPTByStage(userId: str, Stype: str, userText: str) -> str:
    
    stage = getStage(Stype)

    botReply: str = ""
    systemPrompt = genSystemPrompt(stage)
    
    
    prompts = [{
        "role": "system",
        "content": systemPrompt
    }]
    prompts.append({
                    "role": "user",
                    "content": userText
                })
    # botReply += "\n***"+"\n***".join([str(unit) for unit in prompts])
    botReply += "\n"+callGpt(prompts, 0.3)

    if "continuer" in stage.action:
        botReply +="\n"+stage.action["continuer"]
    return botReply       


