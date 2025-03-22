import cv2
import os
import datetime
from enum import Enum
import time
from PIL import Image
import numpy as np
import io
import base64

class LogLevel(Enum):
    NONE = 0
    BASIC = 1
    VERBOSE = 2
    SNAPSHOT = 3  # Save all snapshots with timestamps


import threading




class DroidCamHandler:
    def __init__(self, ip_address, log_level=LogLevel.BASIC, snapshot_dir="snapshots"):
        if not ip_address.startswith("http://"):
            ip_address = f"http://{ip_address}"
        if not ip_address.endswith("/video"):
            ip_address = f"{ip_address}/video"

        self.ip_address = ip_address
        self.cap = None
        self.log_level = log_level
        self.snapshot_dir = snapshot_dir
        self.latest_frame = None  # Store the latest frame
        self.streaming = False  # Flag to control the background thread

        if self.log_level == LogLevel.SNAPSHOT and not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)
            self._log(f"Created snapshot directory: {self.snapshot_dir}")

        self.open_stream()

    def _log(self, message, level=LogLevel.BASIC):
        if level.value <= self.log_level.value:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] DroidCam: {message}")

    def _update_frames(self):
        """Continuously updates the latest frame in a background thread."""
        while self.streaming and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.latest_frame = frame  # Store the most recent frame
            time.sleep(0.001)  # Tiny delay to avoid overloading the CPU

    def open_stream(self):
        """Opens the stream and starts the background thread for frame updates."""
        self.cap = cv2.VideoCapture(self.ip_address)
        if not self.cap.isOpened():
            self._log(f"Error: Couldn't open DroidCam stream at {self.ip_address}", LogLevel.BASIC)
            return False

        self.streaming = True
        threading.Thread(target=self._update_frames, daemon=True).start()  # Start the background frame update thread
        self._log(f"Stream opened successfully", LogLevel.SNAPSHOT)
        return True

    def stream_video(self, window_name="DroidCam Stream"):
        """Displays the video stream."""
        if self.cap is None:
            if not self.open_stream():
                return

        self._log(f"Streaming video from {self.ip_address}")
        self._log("Press 'q' to exit the stream")

        while self.streaming:
            if self.latest_frame is not None:
                cv2.imshow(window_name, self.latest_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.streaming = False
                break

        cv2.destroyWindow(window_name)
        self._log("Stream display closed", LogLevel.VERBOSE)

    def take_snapshot(self, compression: int = 100) -> Image:
        """
        Takes a snapshot of the latest frame being streamed, rotates it left,
        optionally compresses it, saves it if verbosity is high, and returns a PIL image.

        Args:
            compression (int): Compression level (percentage of original size).
                               100 = No compression, 50 = Half size, etc.

        Returns:
            PIL.Image.Image: The compressed image object if successful, otherwise None.
            str: File path of the saved snapshot if saved, otherwise None.
        """
        if self.latest_frame is None:
            self._log("Error: No frame available for snapshot.", LogLevel.BASIC)
            return None

        frame = self.latest_frame.copy()
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate left

        # Convert OpenCV image (NumPy array) to PIL image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Apply compression (resize image)
        if 0 < compression < 100:
            width, height = image.size
            new_width = int(width * (compression / 100))
            new_height = int(height * (compression / 100))
            image = image.resize((new_width, new_height), 3)

        # Save compressed image using `save_snapshot`
        saved_path = None
        if self.log_level == LogLevel.SNAPSHOT:
            success, saved_path = self.save_snapshot(frame=cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
            if success:
                print(f"Compressed snapshot saved at: {saved_path}")

        return image

    def save_snapshot(self, filename=None, frame=None):
        """
        Saves a snapshot as a PNG file and returns the file path.

        Args:
            filename (str, optional): The filename to save the snapshot to.
            frame (numpy.ndarray, optional): The frame to save. If None, takes a new snapshot.

        Returns:
            bool: True if successful, False otherwise.
            str: Path to the saved file if successful, None otherwise.
        """
        try:
            if filename is None:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = os.path.join(self.snapshot_dir, f"snapshot_{timestamp}.png")  # Save as PNG

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            # Convert OpenCV image (NumPy array) to PIL image
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image.save(filename, format="PNG")  # Save as PNG

            self._log(f"Snapshot saved to {filename}")

            return True, filename
        except Exception as e:
            self._log(f"Error saving snapshot: {e}", LogLevel.BASIC)
            return False, None

    def close(self):
        """
        Closes the connection to the DroidCam stream and cleans up resources.

        Returns:
            None
        """
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            cv2.destroyAllWindows()
            self._log("DroidCam connection closed.", LogLevel.VERBOSE)
        self.cap = None


# Function to encode the image from a PIL object
def encode_image_pil(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")  # Save as JPEG format
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


if __name__ == "__main__":
    droidcam_ip = "10.0.1.18:4747"

    # Initialize the camera
    print(f"Connecting to DroidCam at {droidcam_ip}...")
    droidcam = DroidCamHandler(droidcam_ip, log_level=LogLevel.SNAPSHOT)
    # droidcam.stream_video()


    while True:
        input("Press something to take a snapshot: ")
        droidcam.take_snapshot()
