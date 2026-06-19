import requests

url = "http://localhost:11434/api/chat"

payload = {
    "model": "llama3",
    "prompt": "Explain Docker in interview-ready language",
    "stream": False
}

response = requests.post(url, json=payload)
# print(response.json()["response"])
print(response.json())