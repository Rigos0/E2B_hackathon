from ..functions import BaseFunction

from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv
import json

load_dotenv()


class ExecutePythonFunction(BaseFunction):
    """
    Function to execute Python code in a sandbox.
    """

    def __init__(self, robot):
        self.robot = robot

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
        self.robot.beep()

        print(f"Executing the code: {code}")
        with Sandbox() as sandbox:
            execution = sandbox.run_code(code)
            result = execution.text

        print(f"Execution: {result}")

        return result

import random


class GenerateRandomNumberFunction(BaseFunction):
    """
    Function to generate a random number between 1 and a specified upper bound.
    """

    function_schema = {
        "type": "function",
        "function": {
            "name": "generate_random_number",
            "description": "Generates a random number between 1 and a specified upper bound.",
            "parameters": {
                "type": "object",
                "properties": {
                    "upper_bound": {
                        "type": "integer",
                        "description": "The upper bound for the random number (inclusive)."
                    }
                },
                "required": ["upper_bound"],
                "additionalProperties": False
            },
            "strict": True
        }
    }

    def execute(self, upper_bound: int):
        """
        Generates and returns a random number between 1 and the specified upper bound.

        Args:
            upper_bound (int): The upper bound for the random number (inclusive).

        Returns:
            str: A random number between 1 and upper_bound, as a string.
        """
        # Convert to int in case it comes in as a string
        upper_bound = int(upper_bound)
        result = random.randint(1, upper_bound)
        print(f"Generated random number between 1 and {upper_bound}: {result}")
        return str(result)

if __name__ == "__main__":
    execute_python = ExecutePythonFunction()

    code = "import math\\nresult = math.factorial(16)\\nresult"

    print(execute_python.execute(code))
