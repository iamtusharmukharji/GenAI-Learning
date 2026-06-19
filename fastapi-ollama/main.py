from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from ollama import Client


app = FastAPI(

    title="API Service with local LLM"
)

ollama_client = Client(
    host="http://localhost:11434"
)
system_instruction = '''you are a chatbot that turns an RGB led to the color specified by the user query. You will only respond
with the RGB values in the format {"sucess":true, data: [R, G, B], message:<some user friendly message>}. Do not include any other text in your response.
If user query is not a color related, respond with {"success": false, "data": null, message:<some user friendly message>}'''



@app.get('/')
async def root():
    return RedirectResponse('/docs')


@app.get('/llm')
async def chat_llm(promt:str):
     
    llm_resp = ollama_client.chat(
        model= "gemma:2b",
        messages= [
            {"role":"system", "content":system_instruction},
            {"role":"user", "content":promt}
        ]
    )

    return {"success":True, "response":llm_resp.message.content}
     




