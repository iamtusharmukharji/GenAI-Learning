from openai import OpenAI
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cred_loader import creds



# Gemini APIs can be accessed using the OpenAI Python SDK by specifying the appropriate model name.
# For example, to use the Gemini-2.5 Flash model, you can specify "gemini-2.5-flash" as the model name when making API calls.

client = OpenAI(
    api_key=creds.api_key.get("GEMNI_API_KEY"),
    base_url=creds.api_key.get("GEMNI_API_URL")
)

system_instruction = '''you are a chatbot that turns an RGB led to the color specified by the user query. You will only respond
with the RGB values in the format {"sucess":true, data: [R, G, B], message:<some user friendly message>}. Do not include any other text in your response.
If user query is not a color related, respond with {"success": false, "data": null, message:<some user friendly message>}'''

user_query = "change the color to purple"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_query}
    ]
)
# print(dir(response.choices[0]))
print(response.choices[0].message.content)