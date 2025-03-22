# from ..functions import BaseFunction

from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv
import json

load_dotenv()


class ExecutePythonFunction():
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
                "required": ["code"]
            }
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


if __name__ == "__main__":
    execute_python = ExecutePythonFunction()

    code = "import math\\nresult = math.factorial(16)\\nresult"

    print(execute_python.execute(code))
