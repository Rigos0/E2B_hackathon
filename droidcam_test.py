import time

from droidcam.core import *
from llm_agent.llm import *

llm = OpenAIModel()

droidcam = DroidCamHandler(ip_address="10.113.131.127:4747",
                           log_level=LogLevel.SNAPSHOT)

time.sleep(3)

def get_front_camera_image_message(droidcam_object):
    """Captures an image from the front camera and returns it as a message."""
    image = droidcam_object.take_snapshot()
    base64_image = encode_image_pil(image)

    return {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"View from robot front camera.",
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "low",
                },
            },
        ],
    }


image_message = [get_front_camera_image_message(droidcam)]
response = llm.complete(image_message)
print(response)