from openai import OpenAI
from cred_loader import creds


# Gemini APIs can be accessed using the OpenAI Python SDK by specifying the appropriate model name.
# For example, to use the Gemini-2.5 Flash model, you can specify "gemini-2.5-flash" as the model name when making API calls.

client = OpenAI(
    api_key=creds.api_key.get("GEMNI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is an AI system?"}
    ]
)
print(dir(response.choices[0]))
# print(response.choices[0].message.content)