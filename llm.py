import json
import os
from typing import Any

from xai_sdk import Client
from xai_sdk.chat import system, tool, tool_result, user

from utils import get_topics


def query_agent(query: str):
    client = Client(api_key=os.getenv("XAI_API_KEY"))

    tools = [
        tool(
            name="print_output",
            description="Print text for user. This must be used at least once in every single conversation to output some content for the user to see, but feel free to use it more often as needed.",
            parameters={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content to print"},
                },
                "required": ["content"],
            },
        ),
        tool(
            name="get_topics",
            description="Get the list of current topics in the wiki",
            parameters={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]

    chat = client.chat.create(model="grok-4-1-fast-reasoning", tools=tools)

    chat.append(
        system(
            "You are Grok, a highly intelligent, helpful AI assistant. Be concise and powerful."
        ),
    )
    chat.append(user(query))
    response = chat.sample()

    while response.tool_calls:
        chat.append(response)
        for tc in response.tool_calls:
            args = json.loads(tc.function.arguments)
            if tc.function.name == "print_output":
                print(args["content"])
                chat.append(tool_result("Output printed!"))
            elif tc.function.name == "get_topics":
                topics = get_topics()
                chat.append(tool_result(json.dumps(topics)))
        response = chat.sample()
    return response.content
