from openai import OpenAI
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from cred_loader import creds


# Chain Of Thought(COT) prompting example

client = OpenAI(
    api_key=creds.api_key.get("GEMNI_API_KEY"),
    base_url=creds.api_key.get("GEMNI_API_URL")
)

'''Chain of Thought (CoT) is a reasoning technique where an LLM breaks a problem into 
intermediate steps before producing the final answer. It improves performance on 
complex tasks such as mathematics, logic, planning, and coding. Modern models like 
GPT-5 and Gemini perform much of this reasoning internally through hidden chain-of-thought
mechanisms, so developers often no longer need to explicitly prompt the model to 
"think step by step.'''

SYS_PROMPT = '''You are an AI assistant which responds to user queries like informational
info, solves mathematics or logical problems and uses tools if requires.
Response structure must be like below

{"step":"PLAN | TOOL | OUTPUT | OBSERVE", "content":"text", }

Available Tools:
    * call_wttr_api
    * move_robot

Example 1
User Query : What is sum of 2+4

{"step":"PLAN", "content":"User is aksing to solve a mathemetical problem"}
{"step":"PLAN", "content":"Reading equation 2+4"}
{"step":"PLAN", "content":"Solve 2+4 = 6" }
{"step":"OUTPUT", "content":"Final result of 2 + 4 = 6" }

Example 2
User Query : What is the weather of Delhi

{"step":"PLAN", "content":"User is aksing about weather of Delhi"}
{"step":"PLAN", "content":"check for available tools" }
{"step":"TOOL", "tool_name" : "call_wttr_api", "input":"Delhi" }
{"step":"OBSERVE", "tool_name" : "call_wttr_api", "output":"Partly Cloudy  +35°C" }
{"step":"PLAN", "content":"Yes,  got the weather info its Partly Cloudy and temperature is 35°C" }
{"step":"OUTPUT", "content":"The current weather of Delhi is Partially cloudy and having temperature of 35°C" }

'''


USER_PROMPT = "Who is Arijit Singh?"


response = client.chat.completions.create(
    model="gemini-2.5-flash-lite",
    messages=[
        {"role": "system", "content": SYS_PROMPT},
        {"role": "user", "content": USER_PROMPT}
    ]
)

print(response.choices[0].message.content)