from droidcam.core import *
from llm_agent.logic import *
import time


llm = OpenAIModel()

# droidcam_ip = "10.113.131.127:4747"
# droidcam = DroidCamHandler(droidcam_ip,
#                            log_level=LogLevel.SNAPSHOT)
#
# time.sleep(3)
# image = droidcam.take_snapshot()
# base64_image = encode_image_pil(image)

# messages = [
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": f"data:image/jpeg;base64,{base64_image}",
#                                 "detail": "low",
#                             },
#                         },
#                         {
#                             "type": "text",
#                             "text": "What do you see in this image?",
#                         },
#                     ],
#                 }
#             ]

messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Try executing python code to find what the factorial of 16! Also, use the generate random number tool and give me also the random number.",
                        },
                    ],
                }
            ]

response, messages = llm.complete(messages=messages)

print("\n\n\n")
print("Messages: ")
for m in messages:
    print(m)

