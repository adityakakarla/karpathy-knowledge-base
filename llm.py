import os

from xai_sdk import Client
from xai_sdk.chat import system, user


def base_llm(query):
    client = Client(api_key=os.getenv("XAI_API_KEY"))
    chat = client.chat.create(model="grok-4-1-fast-non-reasoning")
    chat.append(
        system(
            "You are Grok, a highly intelligent, helpful AI assistant. Be concise and powerful."
        )
    )
    chat.append(user(query))
    response = chat.sample()
    return response.content
