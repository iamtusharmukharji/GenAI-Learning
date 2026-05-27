from openai import OpenAI
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cred_loader import creds


# Few shot prompting example

client = OpenAI(
    api_key=creds.api_key.get("GEMNI_API_KEY"),
    base_url=creds.api_key.get("GEMNI_API_URL")
)

'''Few shot prompting is a prompting technique where you provide the model with a task description, input,
 and a few examples of the desired output. The model uses these examples to understand the task better and generate
a more accurate response.'''

SYS_PROMPT = "You are a bot that answers questions related to physics else say IDK."


USER_PROMPT = "Who is Arijit Singh?"


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYS_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ]
)

print(response.choices[0].message.content)