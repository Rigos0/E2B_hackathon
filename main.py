from droidcam.core import *
from llm_agent.messages import *
import time


llm = OpenAIModel()

droidcam_ip = "10.113.131.127:4747"
droidcam = DroidCamHandler(droidcam_ip,
                           log_level=LogLevel.SNAPSHOT)

time.sleep(3)
image = droidcam.take_snapshot()
base64_image = encode_image_pil(image)

messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "low",
                            },
                        },
                        {
                            "type": "text",
                            "text": "What do you see in this image?",
                        },
                    ],
                }
            ]

response = llm.complete(messages=messages)
print(response.choices[0].message.content)
print(response)

