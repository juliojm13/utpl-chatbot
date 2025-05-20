import os
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = GoogleGenerativeAI(google_api_key=GOOGLE_API_KEY, model="models/gemini-2.0-flash")

def get_gemini_response(prompt: str, history: list) -> str:
    # history: list of dicts with 'role' and 'content'
    # For simplicity, concatenate history and prompt
    context = "\n".join([f"{m['role']}: {m['content']}" for m in history])
    full_prompt = f"{context}\nuser: {prompt}\nbot:"
    return llm(full_prompt) 