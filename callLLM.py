import requests
import json


def call(user_input, max_tokens = 300):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer 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",
            
        },
        data=json.dumps({
            "model": "z-ai/glm-4.5-air:free", # Optional
            "messages": user_input,
            "max_tokens": max_tokens
        })
        )
    response = response.json()
    print(response["choices"][0]["message"]["content"])
    
    return response["choices"][0]["message"]["content"], response["choices"][0]["message"]
