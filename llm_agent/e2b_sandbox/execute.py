from ..functions import BaseFunction

from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv
import json

load_dotenv()


class ExecutePythonFunction(BaseFunction):
    """
    Function to execute Python code in a sandbox.
    """

    function_schema = {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Execute python code in a Jupyter notebook cell and return result",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "The python code to execute in a single cell."
                    }
                },
                "required": ["code"],
                "additionalProperties": False
            },
            "strict": True
        }
    }

    def execute(self, code: str):
        code = code.replace("\\n", "\n")

        print(f"Executing the code: {code}")
        with Sandbox() as sandbox:
            execution = sandbox.run_code(code)
            result = execution.text

        print(f"Execution: {result}")

        return result

import random


class GenerateRandomNumberFunction(BaseFunction):
    """
    Function to generate a random number between 1 and 100.
    """

    function_schema = {
        "type": "function",
        "function": {
            "name": "generate_random_number",
            "description": "Generates a random number between 1 and 100.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        }
    }

    def execute(self):
        """
        Generates and returns a random number between 1 and 100.
        """
        result = random.randint(1, 100)
        print(f"Generated random number: {result}")
        return str(result)


if __name__ == "__main__":
    execute_python = ExecutePythonFunction()

    code = "import math\\nresult = math.factorial(16)\\nresult"

    print(execute_python.execute(code))
