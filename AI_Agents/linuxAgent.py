from openai import OpenAI
import requests
from cred_loader import creds
import json
from pydantic import BaseModel, Field
from typing import Optional
import subprocess


llm_client = OpenAI(
    api_key= creds.api_key["GEMNI_API_KEY"],
    base_url= creds.api_key["GEMNI_API_URL"]
)

class LLMOutputSchema(BaseModel):
    step : str = Field(..., description="The step ID of the llm executing")
    content: Optional[str] = Field(None, description="The content produced via llm response")
    tool : Optional[str] =  Field(None)
    input : Optional[str] = Field(None)



SYS_PROMPT = '''You are an AI assistant which responds to user queries like informational
info, solves mathematics or logical problems and uses tools if requires.

Response structure must be like below

{"step":"PLAN | TOOL | OUTPUT | OBSERVE", "content":"text"}

Available Tools:
    * call_wttr_api
    * move_robot
    * run_linux_commands



Example 1
User Query : What is sum of 2+4

{"step":"PLAN", "content":"User is aksing to solve a mathemetical problem"}
{"step":"PLAN", "content":"Reading equation 2+4"}
{"step":"PLAN", "content":"Solve 2+4 = 6" }
{"step":"OUTPUT", "content":"Final result of 2 + 4 = 6" }

Example 2
User Query : What is the weather of Delhi

{"step":"PLAN", "content":"User is asking about weather of Delhi"}
{"step":"PLAN", "content":"check for available tools" }
{"step":"TOOL", "tool_name" : "call_wttr_api", "input":"Delhi" }
{"step":"OBSERVE", "tool_name" : "call_wttr_api", "output":"Partly Cloudy  +35°C" }
{"step":"PLAN", "content":"Yes,  got the weather info its Partly Cloudy and temperature is 35°C" }
{"step":"OUTPUT", "content":"The current weather of Delhi is Partially cloudy and having temperature of 35°C" }

Example 3
User Query : Create a function.py file in current directory

{"step":"PLAN", "content":"User is requesting for creating a file in current directory"}
{"step":"PLAN", "content":"check for available tools" }
{"step":"TOOL", "tool_name" : "run_linux_commands", "input":"touch function.py" }
{"step":"OBSERVE", "tool_name" : "run_linux_commands", "output":"file is created"} or {"step":"OBSERVE", "tool_name" : "run_linux_commands", "output":"error in file creation"}
{"step":"PLAN", "content":"Yes,  the file is created" } or {"step":"PLAN", "content":"There is some error in file creation"}
{"step":"OUTPUT", "content":"your file has been created" } or {"step":"OUTPUT", "content":"file could not be created" }


Important Rules:
    - Return only one JSON object at a time
    - "OBSERVE" step will be given by program so you need to wait
'''

def call_wttr_api(city_name :str) -> str :

    api_url = f"https://wttr.in/{city_name.lower()}?format=%C+%t"
    
    api_resp = requests.get(api_url)
    
    if api_resp.status_code == 200:
        return api_resp.text
    
    return "OOPs! Error fetching weather"


def run_linux_commands(cmd):
    try:
        result = subprocess.run([
            r"C:\Program Files\Git\bin\bash.exe",
            "-c",
            cmd
            ],
            capture_output=True,
            text=True
        )
        
        if result:
            return result.stdout
        return True

    except Exception as err:
        return str(err)

tool_list = {
    "call_wttr_api" : call_wttr_api,
    "run_linux_commands" : run_linux_commands
}

class LLMOutputSchema(BaseModel):
    step : str = Field(..., description="The step ID of the llm executing")
    content: str | None = None
    tool_name: str | None = None
    input: str | None = None

def run_agent():

    user_query = input(">>  ")
    message_logs = [
        {"role":"system", "content" : SYS_PROMPT},
        {"role":"user", "content" : user_query}
    ]
    while True:
        response = llm_client.chat.completions.parse(
            model = "gemini-2.5-flash",
            response_format= LLMOutputSchema,
            messages= message_logs
        )
        # if output format is not given as any pydantic class then we need to get the response text as below 
        # llm_text = response.choices[0].message.content

        # if output format is defined as any pydantic class then we need to get the response text as below
        # but as this is Gemini model we need to get the raw string because gemini model gives jsons at once 
        llm_parsed = response.choices[0].message.parsed

        llm_text = response.choices[0].message.content

        print(llm_parsed)
        message_logs.append({"role":"assistant", "content":llm_text})
        # parsed_text = llm_text.split('\n')[-1]
        # parsed_json = json.loads(parsed_text)
        # parsed_json = dict(llm_parsed)
        if llm_parsed.step == 'TOOL':
            tool_arg = llm_parsed.input
            tool = tool_list.get(llm_parsed.tool_name)
            tool_res = tool(tool_arg)
            print("TOOL Response >>>", tool_res)
            msg = {"step":"OBSERVE", "tool_name" : llm_parsed.tool_name, "output":tool_res }
            
            message_logs.append({
                "role":"user",
                "content" : json.dumps(msg)
            })
            continue

        if llm_parsed.step == "OUTPUT":
            print(llm_parsed.content)
            break


    
   



run_agent()