import requests
import json
import dotenv
import os

dotenv.load_dotenv()

def call(chat_memory, max_tokens = 300, model = 'meta-llama/llama-3.2-1b-instruct'):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            
        },
        data=json.dumps({
            "model": model, 
            "messages": chat_memory,
            "max_tokens": max_tokens
        }))
    
    response = response.json()
    print(response)
    print("")
    try:
        print(response["choices"][0]["message"]["content"])
    except:
        print(response["error"])
    print("")
    
    return response["choices"][0]["message"]["content"]

if __name__ == '__main__':
    print(call([{"role": "system", "content": "you are GlaD0s from the video game Portal"}, {"role": "user", "content": "hello"}]))