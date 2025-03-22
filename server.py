"""
Server running on the ev3 brick.

- Receives commands and executes them on the robot.
"""

import socket
import threading
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MediumMotor
from ev3dev2.sound import Sound

# Initialize motors and sound
tank_drive = MoveTank(OUTPUT_B, OUTPUT_C)
medium_motor = MediumMotor(OUTPUT_D)  # Initialize the medium motor on port D
sound = Sound()

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))  # Listen on all interfaces, port 12345
server_socket.listen(1)
print("EV3 Server Started! Waiting for commands...")


# Define playsound mappings
playsound_paths = {
    "oiai": "/home/robot/myproject/oiai.wav",
    "intro": "/home/robot/myproject/intro.wav"
}


# Function to play sound file in a separate thread
def play_sound_file(filename):
    try:
        sound.play_file(filename)
        print("Finished playing")
    except Exception as e:
        print("Error playing sound file", e)


# Accept a connection
client_socket, client_address = server_socket.accept()
print("Connected to", client_address)

# Command handling loop
try:
    while True:
        command = client_socket.recv(1024).decode().strip()  # Receive command
        if not command:
            continue  # If empty, keep listening

        print("Received command:", command)

        # Split the command string by spaces
        parts = command.split()
        cmd = parts[0]

        # Check if there's an optional time parameter for movement commands
        duration = 2  # Default duration
        if len(parts) > 1 and cmd in ["forward", "backward", "left", "right"]:
            try:
                duration = float(parts[1])
            except ValueError:
                # If conversion fails, use default
                print("Invalid time parameter. Using default 2 seconds.")

        # Movement commands with optional duration parameter
        if cmd == "forward":
            tank_drive.on_for_seconds(SpeedPercent(-30), SpeedPercent(-30), duration)

        elif cmd == "backward":
            tank_drive.on_for_seconds(SpeedPercent(30), SpeedPercent(30), duration)

        elif cmd == "left":
            tank_drive.on_for_seconds(SpeedPercent(-20), SpeedPercent(20), duration)

        elif cmd == "right":
            tank_drive.on_for_seconds(SpeedPercent(20), SpeedPercent(-20), duration)

        elif cmd == "stop":
            tank_drive.off()

        # Dance command using the medium motor on port D
        elif cmd == "dance":
            # Make a simple dance routine using the medium motor and tank drive
            sound.speak("Time to dance")

            # Spin the medium motor back and forth
            for _ in range(2):
                medium_motor.on_for_seconds(SpeedPercent(50), 0.5)
                medium_motor.on_for_seconds(SpeedPercent(-50), 0.5)

            # Final pose
            tank_drive.off()
            medium_motor.off()
            sound.beep()

        elif cmd == "beep":
            sound.beep()

        elif command.startswith("say: "):
            text_to_say = command[5:]  # Remove "say: " prefix
            print("Saying:", text_to_say)
            sound.speak(text_to_say)

        elif cmd == "playsound":
            if len(parts) > 1:
                sound_flag = parts[1]
                sound_file = playsound_paths.get(sound_flag, None)
                if sound_file:
                    print("Playing sound")
                    sound_thread = threading.Thread(target=play_sound_file, args=(sound_file,))
                    sound_thread.daemon = True
                    sound_thread.start()
                else:
                    print("Invalid sound flag. Available flags: oiai, intro")
            else:
                print("Missing sound flag. Usage: playsound <flag>")

        elif cmd == "quit":
            break  # Stop the server

except ConnectionResetError:
    print("Client disconnected.")
except Exception as e:
    print("Error:", e)

# Cleanup
print("Closing connection...")
client_socket.close()
server_socket.close()