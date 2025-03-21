from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.environ.get("OPEN_AI_KEY")

client = OpenAI(api_key=openai_api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://transform.octanecdn.com/fit/1600x900/https://octanecdn.com/colorvisionprintingcom/colorvisionprintingcom_370928206.png",
                    "detail": "low"
                },
            },
        ],
    }],
)

print(response.choices[0].message.content)

print(response)