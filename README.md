# RASA
The project was forked from [rasa-bot](https://github.com/Chunshan-Theta/Mentor-MBTI).

This is a mentor bot that can help to introduce the discussion event and teach the user how to discussion, built with the rasa framework and LLM. 
We design ideas from ChatDev and try to build a step-by-step framework. 

# Design

```

actions:
    - action_introduce_the_bot
    - action_introduce_nuclear_power
    - action_introduce_discussion
    - action_trying_asking
    - action_trying_replying
    - action_summary
    - action_set_to_intro_nuclear_power
    - action_set_to_intro_discussion
    - action_set_to_try_ask
    - action_set_to_try_reply
		- action_set_summary
    - utter_ask_next_step (say "ok" if you don't have other questions)

intents:
    - faq
    - hi
    - confirm

slots:
  stage:
    type: string
    initial_value: "intro_bot"
    mappings:
      - type: custom

- regex: confirm
  examples: |
    - ^/OK.*$
    - ^/好的.*$
    - ^/繼續.*$



- story: (intro_bot)_01
  steps:
     - slot_was_set:
       - stage: (intro_bot)
     - intent: hi
     - action: action_introduce_the_bot
     - action: utter_ask_next_step
     - intent: confirm
     - action: action_set_to_intro_nuclear_power

- story: (intro_bot)_02
  steps:
     - slot_was_set:
       - stage: (intro_bot)
     - intent: hi
     - action: action_introduce_the_bot
     - action: utter_ask_next_step
     - intent: faq
     - action: action_introduce_the_bot
     - action: utter_ask_next_step
     - intent: faq
     - action: action_introduce_the_bot
     - intent: confirm
     - action: action_set_to_(intro_nuclear_power)
```

- RAG

```
action_introduce_the_bot:
  examples:
      - user: hi
        agent: hello! following me to learn how to discuss with other people in a good environment.
      - user: how do you be made?
        agent: I built by Rasa and ChatGpt. It's open-source, you can check in GitHub.
      - user: Who are you?
        agent: I'm an interactive bot designed to support you in knowing the discussion policies

action_introduce_nuclear_power
  examples:
      - user: ok
        agent: Hi, I want to talk about nuclear power with you. ... 
			- user: hi
        agent: Hi, I want to talk about nuclear power with you. ... 
			- user: What is status of the nuclear power in Taiwan?
        agent: Taiwan heavily relies on other energy sources like coal... 
action_introduce_discussion
  examples:
      - user: ok
        agent: Hi, I want to talk about discussion policies with you. ... 
action_trying_asking
  examples:
      - user: ok
        agent: Hi, In this stage, we can try to ask a question in polite. ... 
action_trying_replying
  examples:
      - user: ok
        agent: Hi, In this stage, we can try to reply to a question in a polite. ... 
action_summary
  examples:
      - user: ok
        agent: Hi, I want to talk about nuclear power with you. ... 
```

### UI Demo

![img](./doc/chatroom_01.png)


### Game Demo

```
```

# Service

### Start Service
1. Update OpenAI API Key in docker-compose.yml
2. Update Domain name in botroom/App.js:23 -> (frontend)
3. up service with docker-compose
```
docker-compose up
```
4. go to weeb
```
http://127.0.0.1
```

### Ask bot by cmd
```
curl -o output.txt -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"sender": "user-001","message": "早安"}'  http://127.0.0.1:5005/webhooks/rest/webhook && echo -e "$(<output.txt)"
curl -o output.txt -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"sender": "user-001","message": "昆蟲是甚麼?"}'  http://127.0.0.1:5005/webhooks/rest/webhook && echo -e "$(<output.txt)"
curl -o output.txt -X POST -H "Content-Type: application/json; charset=UTF-8" -d '{"sender": "user-001","message": "是的"}'  http://127.0.0.1:5005/webhooks/rest/webhook && echo -e "$(<output.txt)"
```


# Testing
- with rasa tests
```
docker-compose up test-model
```

- interactive
```
docker run -it -v ./actionsServer:/app rasa/rasa:3.6.6-full interactive
```

