from asciimatics.screen import Screen
from PIL import Image
import os
import time

class SusCommand:
    def __init__(self):
        self.name = "sus"
        self.parameters = []
        self.descr = "Displays a sus animation"

    def run(self, *args):
        gif_path = os.path.join(os.path.dirname(__file__), 'sus/sus.gif')

        # Load the GIF
        gif = Image.open(gif_path)
        frames = []
        try:
            while True:
                frames.append(gif.copy())
                gif.seek(len(frames))  # Move to the next frame
        except EOFError:
            pass

        # Convert frames to ASCII
        ascii_frames = [self._image_to_ascii(frame) for frame in frames]

        # Display the animation
        self._display_animation(ascii_frames)

    def _image_to_ascii(self, image, new_width=80):
        # Resize image while maintaining aspect ratio
        width, height = image.size
        aspect_ratio = height / float(width)
        new_height = int(aspect_ratio * new_width * 0.55)
        image = image.resize((new_width, new_height))

        # Convert image to grayscale
        image = image.convert('L')
        pixels = image.getdata()

        # ASCII characters used to build the output text
        ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

        # Map each pixel to an ASCII char
        ascii_str = "".join([ascii_chars[pixel // 25] for pixel in pixels])
        ascii_str_len = len(ascii_str)
        ascii_img = "\n".join([ascii_str[i:i + new_width] for i in range(0, ascii_str_len, new_width)])

        return ascii_img

    def _display_animation(self, frames):
        screen = Screen.open()

        try:
            last_refresh_time = time.time()
            frame_index = 0
            while True:
                # Check if it's time to refresh the screen
                current_time = time.time()
                if current_time - last_refresh_time >= 0.1:  # Refresh every 0.1 seconds
                    frame = frames[frame_index % len(frames)]
                    screen.clear()
                    lines = frame.split('\n')
                    for i, line in enumerate(lines):
                        screen.print_at(line, 0, i)
                    screen.refresh()

                    # Update last refresh time and frame index
                    last_refresh_time = current_time
                    frame_index += 1

                # Check for input events
                ev = screen.get_event()
                if ev is not None:
                    return

                # Sleep briefly to avoid high CPU usage
                time.sleep(0.01)

        finally:
            screen.close()

