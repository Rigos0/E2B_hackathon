import socket
import time
import threading
import re
from typing import Optional
from ..functions import BaseFunction


class RobotController:
    def __init__(self, ip: str, port: int = 12345):
        """
        Initializes the RobotController with a persistent connection.

        Args:
            ip: The IP address of the robot.
            port: The port number for the connection (default: 12345).
        """
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connect()

    def _connect(self):
        """Establishes a connection to the robot."""
        try:
            self.socket.connect((self.ip, self.port))
        except Exception as e:
            print(f"Error connecting to robot: {e}")

    def send_command(self, command: str) -> Optional[str]:
        """
        Sends a command to the robot over the persistent connection.

        Args:
            command: The command to send (e.g., "forward", "backward", "left", "right", "say: Hello").

        Returns:
            Confirmation message or error if connection fails.
        """
        try:
            self.socket.sendall(command.encode())
            time.sleep(0.1)
            return f"Sent command: {command}"
        except Exception as e:
            return f"Error sending command: {str(e)}"

    def send_command_async(self, command: str):
        """Runs send_command in a separate thread to avoid blocking execution."""
        thread = threading.Thread(target=self.send_command, args=(command,))
        thread.daemon = True
        thread.start()

    def move(self, command: str) -> str:
        """
        Moves the robot in the given direction with an optional duration.

        Args:
            command: A string containing the direction ('forward', 'backward', 'left', 'right', 'dance')
                     optionally followed by a duration in seconds (e.g., 'forward 2').

        Returns:
            Confirmation message.
        """
        valid_directions = {"forward", "backward", "left", "right", "dance"}
        parts = command.split()
        direction = parts[0]
        duration = 2  # Default duration

        if direction not in valid_directions:
            return "Invalid direction. Choose from: forward, backward, left, right, dance."

        if len(parts) > 1:
            try:
                duration = float(parts[1])
            except ValueError:
                return "Invalid duration. Please provide a valid number of seconds."

        return self.send_command(f"{direction} {duration}")

    def playsound(self, flag: str) -> str:
        """
        Plays a song on robot speakers based on the given flag.

        Args:
            flag: The sound flag (currently supports 'intro')

        Returns:
            Confirmation message.
        """
        sound_paths = ["intro"]

        if flag not in sound_paths:
            return "Invalid sound flag. Available flags: intro."

        self.send_command_async(f"playsound {flag}")
        return "Playing sound in background."

    @staticmethod
    def clean_response(response: str) -> str:
        """Removes non-basic ASCII characters, keeping letters, numbers, spaces, and dots."""
        return re.sub(r"[^a-zA-Z0-9 .]", "", response)

    def speak(self, message: str) -> str:
        """
        Makes the robot say the given message.

        Args:
            message: The message the robot should say.

        Returns:
            Confirmation message.
        """
        message = self.clean_response(message)
        return self.send_command(f"say: {message}")


class SpeakFunction(BaseFunction):
    """
    Makes the robot speak a given message.

    This function allows the robot to vocalize a message
    """
    function_schema = {
        "type": "function",
        "function": {
            "name": "speak",
            "description": "Make the robot say the given message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The message the robot should say."
                    }
                },
                "required": ["message"],
                "additionalProperties": False
            },
            "strict": True
        }
    }

    def __init__(self, robot: RobotController):
        self.robot = robot

    def execute(self, message: str):
        return self.robot.speak(message)


class MoveFunction(BaseFunction):
    """
    Moves the robot in the specified direction for an optional duration.

    This function controls the robot's movement, allowing it to move forward,
    backward, turn left, or right for a specified duration.
    """
    function_schema = {
        "type": "function",
        "function": {
            "name": "move",
            "description": "Move the robot in a specified direction with an optional duration.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Direction (forward, backward, left, right)."
                    },
                    "duration": {
                        "type": "number",
                        "description": "Duration in seconds for how long the robot should move."
                    }
                },
                "required": ["command", "duration"],
                "additionalProperties": False
            },
            "strict": True
        }
    }

    def __init__(self, robot: RobotController):
        self.robot = robot

    def execute(self, command: str, duration: float = None):
        command_final = command + " " + str(duration)
        return self.robot.move(command_final)


if __name__ == "__main__":
    robot = RobotController("169.254.110.214")
    robot.speak("hello world")
