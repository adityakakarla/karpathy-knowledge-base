import json
import os
from typing import Any

from xai_sdk import Client
from xai_sdk.chat import system, tool, tool_result, user

from utils import add_content_file, get_topics, read_content_file, read_index, update_content_file, update_index


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
        tool(
            name="update_index",
            description="Update the index file for a given topic",
            parameters={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to update the index for",
                    },
                    "new_index": {
                        "type": "string",
                        "description": "The new index content",
                    },
                },
                "required": ["topic", "new_index"],
            },
        ),
        tool(
            name="read_content_file",
            description="Read the contents of a file for a given topic",
            parameters={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic the file belongs to",
                    },
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to read",
                    },
                },
                "required": ["topic", "filename"],
            },
        ),
        tool(
            name="read_index",
            description="Read the index file for a given topic",
            parameters={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to read the index for",
                    },
                },
                "required": ["topic"],
            },
        ),
        tool(
            name="update_content_file",
            description="Update the contents of an existing file for a given topic",
            parameters={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic the file belongs to",
                    },
                    "content": {
                        "type": "string",
                        "description": "The new content to write to the file",
                    },
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to update",
                    },
                },
                "required": ["topic", "content", "filename"],
            },
        ),
        tool(
            name="add_content_file",
            description="Add a new content file for a given topic",
            parameters={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic to add the file to",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file",
                    },
                    "filename": {
                        "type": "string",
                        "description": "The name of the file to create",
                    },
                },
                "required": ["topic", "content", "filename"],
            },
        ),
    ]

    chat = client.chat.create(model="grok-4-1-fast-reasoning", tools=tools)

    chat.append(
        system(
            """You are Grok, a highly intelligent, helpful AI assistant. Be concise and powerful. Notes:

This is a knowledge base management tool.

Please use the get_topics() function to get the current list of topics. Please use the existing topics when passing information to functions that have a topic parameter. Do not try to pass in topics that do not exist, this will lead to failure.

If you are adding new files, you must update the index.
                """
        ),
    )
    chat.append(user(query))
    response = chat.sample()

    while response.tool_calls:
        chat.append(response)
        for tc in response.tool_calls:
            args = json.loads(tc.function.arguments)
            function_name = tc.function.name
            print(f"Invoking {function_name}")
            if function_name == "print_output":
                print(args["content"])
                chat.append(tool_result("Output printed!"))
            elif function_name == "get_topics":
                topics = get_topics()
                chat.append(tool_result(json.dumps(topics)))
            elif function_name == "read_index":
                result = read_index(args["topic"])
                chat.append(tool_result(result))
            elif function_name == "read_content_file":
                result = read_content_file(args["topic"], args["filename"])
                chat.append(tool_result(result))
            elif function_name == "update_index":
                result = update_index(args["topic"], args["new_index"])
                chat.append(tool_result(result))
            elif function_name == "update_content_file":
                result = update_content_file(
                    args["topic"], args["content"], args["filename"]
                )
                chat.append(tool_result(result))
            elif function_name == "add_content_file":
                result = add_content_file(
                    args["topic"], args["content"], args["filename"]
                )
                chat.append(tool_result(result))
        response = chat.sample()
    return response.content
