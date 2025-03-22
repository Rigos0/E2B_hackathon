import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect(("169.254.110.214", 12345))  # Replace with correct IP

while True:
    user_input = input("Enter command: ")
    s.sendall(user_input.encode())  # Convert string to bytes
    time.sleep(2)


# s.sendall(b"""say: To be, or not to be, that is the question:
# Whether tis nobler in the mind to suffer
# The slings and arrows of outrageous fortune,
# Or to take arms against a sea of troubles
# And by opposing end them?""")  # Test command
s.close()

