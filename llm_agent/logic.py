from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Dict, List, Tuple

from .e2b_sandbox.execute import ExecutePythonFunction
import json


class OpenAIModel:
    """
    Communicates with the OpenAI Api
    """
    def __init__(self):
        self.model = "gpt-4o-mini"
        self.default_image_quality = "low"

        load_dotenv()
        openai_api_key = os.environ.get("OPEN_AI_KEY")
        self.client = OpenAI(api_key=openai_api_key)

        # Register available functions
        self.available_tools = {
            "execute_python": ExecutePythonFunction()
        }

    def complete(self, messages: list):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=[tool.function_schema for tool in self.available_tools.values()],
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        print("Initial response: ")
        print(response_message)
        print("\n")

        # Append the model's response to messages to maintain conversation flow
        messages.append({
            "role": "assistant",
            "content": response_message.content,
            "tool_calls": response_message.tool_calls
        })

        # If the model requests a tool execution
        if response_message.tool_calls:
            tool_call_responses = []  # Store tool responses

            for tool_call in response_message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if tool_name in self.available_tools:
                    tool_response = self.available_tools[tool_name].execute(**arguments)

                    # Store tool response
                    tool_call_responses.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,  # Ensure it matches the requested tool call
                        "name": tool_name,
                        "content": tool_response
                    })

            # Append tool response(s) to messages
            messages.extend(tool_call_responses)

            # Re-run the conversation with updated messages
            return self.complete(messages)

        return response, messages

