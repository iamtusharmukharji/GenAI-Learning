from google import genai
from cred_loader import creds


model = "gemini-2.5-flash"

chat = genai.Client(
    api_key=creds.api_key.get("GEMNI_API_KEY")
)  # Initialize the GenAI client with the API key

prompt = "Write a haiku about the changing seasons."

resp = chat.models.generate_content(
    model=model,
    contents=prompt
)

print(resp.text)
