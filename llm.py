import json
import os
from typing import Any

from xai_sdk import Client
from xai_sdk.chat import system, tool, tool_result, user


def query_agent(query: str):
    client = Client(api_key=os.getenv("XAI_API_KEY"))

    tools = [
        tool(
            name="print_output",
            description="Print text for user",
            parameters={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to print"},
                },
                "required": ["content"],
            },
        ),
    ]

    chat = client.chat.create(model="grok-4-1-fast-non-reasoning", tools=tools)

    chat.append(
        system(
            "You are Grok, a highly intelligent, helpful AI assistant. Be concise and powerful."
        ),
    )
    chat.append(user(query))
    response = chat.sample()

    if response.tool_calls:
        chat.append(response)
        for tc in response.tool_calls:
            args = json.loads(tc.function.arguments)
            if tc.function.name == "print_output":
                print(args["content"])
                chat.append(tool_result("Output printed!"))
        response = chat.sample()
    return response.content
