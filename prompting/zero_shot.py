from openai import OpenAI
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cred_loader import creds


# Zero shot prompting example

client = OpenAI(
    api_key=creds.api_key.get("GEMNI_API_KEY"),
    base_url=creds.api_key.get("GEMNI_API_URL")
)

# Zero shot prompting is a prompting technique where you provide the model with a task description and input, without any examples. The model is expected to understand the task and generate an appropriate response based on the provided information.
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