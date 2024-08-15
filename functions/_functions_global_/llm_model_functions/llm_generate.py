import streamlit as st
import requests
import json


class LLMGenerate:
    def __init__(self, talk):
        self.url = "http://localhost:11434/api/chat"
        self.headers = {'Content-Type': "application/json",}
        self.talk = talk

    def beforeSay(self, response):
        return response

    def say(self, response):
        if len(response) == 0:
            return
        self.talk(self.beforeSay(response))

    def generate_response(self, llm_model, prompt, chat_history):
        if len(prompt) == 0:
            return "", chat_history

        full_prompt = []
        for i in chat_history:
            full_prompt.append({
                "role": "user",
                "content": i[0]
            })
            full_prompt.append({
                "role": "assistant",
                "content": i[1]
            })
        full_prompt.append({
            "role": "user",
            "content": prompt
        })

        data = {
            "model": llm_model,
            "stream": True,
            "messages": full_prompt,
        }

        response = requests.post(self.url, headers=self.headers, data=json.dumps(data), stream=True)
        if response.status_code == 200:
            all_response = ''
            this_response = ''
            for line in response.iter_lines():
                if line:
                    jsonData = json.loads(line)
                    this_response += jsonData["message"]['content']
                    if '.' in this_response or '?' in this_response or '!' in this_response:
                        self.say(this_response)
                        all_response += this_response
                        this_response = ''
            if len(this_response) > 0:
                self.say(this_response)
                all_response += this_response
                this_response = ''
            chat_history.append((prompt, all_response))

            # Display the last user message and assistant response on Streamlit
            if chat_history[-1][0]:  # Last user's message
                st.write(f"User: {chat_history[-1][0]}")
            if chat_history[-1][1]:  # Last assistant's message
                st.write(f"Assistant: {chat_history[-1][1]}")

            return "", chat_history
        else:
            return "Error: Unable to fetch response", chat_history
