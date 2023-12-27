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
def callGPTByStage(userId: str, Stype: str, userText: str) -> str:
    
    if Stype == "intro_bot":
        stage = stage_intro_bot
    elif Stype == "intro_unclear_power":
        stage = stage_intro_unclear_power
    elif Stype == "intro_discussion":
        stage = stage_intro_discussion
    elif Stype == "intro_ask":
        stage = stage_try_ask

    elif Stype == "intro_reply":
        stage = stage_try_reply

    else:
        return "callGPTByStage Done."

    botReply: str = ""
    if stage.system == "reply/ans":
        systemPrompt = stage.situation["role"]+stage.situation["task"]+"\n\nplease Reply base on you know.\n you know:\n"
        for unit in stage.target['rag']:
            systemPrompt += "- "+unit[0]+"?"+unit[1]
            systemPrompt += "\n"
        
        prompts = [{
            "role": "system",
            "content": systemPrompt+"\n 請用中文;zh-tw回應;且回應的篇幅必須簡短"
        }]
        prompts.append({
                        "role": "user",
                        "content": userText
                    })
        # botReply += "\n***"+"\n***".join([str(unit) for unit in prompts])
        botReply += "\n"+callGpt(prompts, 0.3)
    elif stage.system == "practice":
        prompts = [{
        "role": "system",
        "content": stage.situation["role"]+stage.situation["task"]
        }]
        for unit in stage.target['rag']:
            prompts.append({
                        "role": "assistant",
                        "content": "\n".join(stage.action["toAgent"])
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
                        "content": "\n".join(stage.action["toAgent"])
                    })
        prompts.append({
                        "role": "user",
                        "content": userText
                    })
        # botReply += "\n***"+"\n***".join([str(unit) for unit in prompts])
        botReply += "\n"+callGpt(prompts, 0.3)
    if "continuer" in stage.action:
        botReply +="\n"+stage.action["continuer"]
    return botReply       


