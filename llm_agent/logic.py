from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Dict, List, Tuple


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

    def complete(self, messages: List[Dict]):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )

        return response

