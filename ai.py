import google.generativeai as ai
from google.generativeai import ChatSession
import os

api_key = os.getenv("GEMINI_TOKEN")



ai.configure(api_key=api_key)

model=ai.GenerativeModel(
  model_name="gemini-1.5-flash",
  system_instruction="ONLY USE ** AS BOLD AND NEW LINE AS RICH TEXT FORMATTING, DONT USE ANYTHING OTHER FORM OF RICH TEXT,You are an specialized assistant for the high seas program from hackclub. Only answer questions regarding coding or the high seas program.")

def start_chat_sesson():
    return model.start_chat()

def get_chat_response(chat: ChatSession, prompt: str) -> str:
    text_response = []
    responses = chat.send_message(prompt, stream=True)
    for chunk in responses:
        text_response.append(chunk.text)
    return "".join(text_response)

print("Ai Online")
