import os
from dotenv import load_dotenv
from langchain_gigachat.chat_models import GigaChat


load_dotenv()
KEY = os.getenv("LLM_API")

LLM = GigaChat(
    credentials=KEY,
    verify_ssl_certs=False,
    model="GigaChat-2-Pro",
    timeout=120, 
    temperature=0,
)

ROLE_OF_MESSAGE = "human" # GigaChat does not accept 'system' messages
