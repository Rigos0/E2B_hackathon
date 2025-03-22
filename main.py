from droidcam.core import *
from llm_agent.llm import *
import time


class MemoryManager:
    def __init__(self, max_steps=5):
        # Stores past iterations, each iteration is a list of messages
        self.iterations = []
        self.last_message_count = 0  # Tracks number of messages before last LLM call
        self.system_prompt = {
            "role": "system",
            "content": "You are a helpful robot assistant. Follow user instructions carefully."
        }
        self.max_steps = max_steps
        self.iteration_number = 0  # Tracks the iteration count

    def add_iteration(self, new_messages):
        """Extracts and stores only new messages as a new iteration (for LLM responses)."""
        new_iteration = new_messages[self.last_message_count:]
        if new_iteration:
            self.iterations.append(new_iteration)
        self.last_message_count = len(new_messages)
        self._trim_memory(self.max_steps)
        self.iteration_number += 1  # Increment after storing LLM response

    def get_memory_as_messages(self):
        """Returns stored memory as a flat list of messages, ensuring system prompt is included."""
        return [self.system_prompt] + [msg for iteration in self.iterations for msg in iteration]

    def _trim_memory(self, steps):
        """Keeps only the last `steps` iterations while preserving the system prompt."""
        if len(self.iterations) > steps:
            self.iterations = self.iterations[-steps:]


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


llm = OpenAIModel()

droidcam = DroidCamHandler(ip_address="10.113.131.127:4747",
                           log_level=LogLevel.SNAPSHOT)
time.sleep(1)


memory = MemoryManager()

# Run multiple iterations
for i in range(5):
    # Step 1: Create new iteration messages
    new_iteration_messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe what is on the camera. Read the text. If there is a task, solve it.",
                },
            ],
        },
        get_front_camera_image_message(droidcam_object=droidcam)
    ]

    # Step 2: Pass stored memory + new iteration messages to LLM
    response, messages = llm.complete(messages=memory.get_memory_as_messages() + new_iteration_messages)

    # Step 3: Store the full step in memory
    memory.add_iteration(messages)

    print("\n\n\n")
    print(f"Iteration {i + 1} Messages: ")
    for m in messages:
        if 'content' in m and isinstance(m['content'], list):
            # Handle the case where content is a list (e.g., with text and image_url)
            filtered_content = []
            for item in m['content']:
                if item.get('type') == 'image_url' and 'image_url' in item:
                    # Replace base64 data with a placeholder
                    url = item['image_url']['url']
                    if 'base64' in url:
                        # Find where the base64 data starts
                        base64_start = url.find('base64,')
                        if base64_start != -1:
                            # Replace the base64 data with a placeholder
                            item = {
                                'type': 'image_url',
                                'image_url': {
                                    'url': url[:base64_start + 7] + ' <BASE64_DATA_HIDDEN>',
                                    'detail': item['image_url'].get('detail', 'low')
                                }
                            }
                filtered_content.append(item)
            content_to_print = filtered_content
        else:
            content_to_print = m.get('content', '')

        # Create a copy of the message with the filtered content
        message_to_print = m.copy()
        message_to_print['content'] = content_to_print

        print(message_to_print)

    print(f"\n\nModel response: {response}")

    print("Sleeping...")
    time.sleep(5)
