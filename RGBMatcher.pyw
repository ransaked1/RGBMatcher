import asyncio
import colorsys
from colorthief import ColorThief
from govee_api_laggat import Govee, GoveeAbstractLearningStorage, GoveeLearnedInfo
from os import getenv
from time import sleep
from typing import Dict
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from logipy import logi_led

# Async function to change Govee RGB device color
async def change_color(api_key, rgb_color, learning_storage):
    # Create new govee object
    govee = await Govee.create(api_key, learning_storage=learning_storage)

    # get_devices is mandatory here!
    devices, err = await govee.get_devices()

    # Turn the light on if it's not and set the color
    for dev in devices:
        success, err = await govee.turn_on(dev.device)
        success, err = await govee.set_color(dev.device, rgb_color)
    await govee.close()

# Dummy class needed for the Govee object
class LearningStorage(GoveeAbstractLearningStorage):
    async def read(self) -> Dict[str, GoveeLearnedInfo]:
        return (
            {}
        )

    async def write(self, learned_info: Dict[str, GoveeLearnedInfo]):
        persist_this_somewhere = learned_info  # save this dictionary to disk

# Get the dominant color from the image
def take_color():
    # Get the top 20 palette colors from wallpaper
    color_thief = ColorThief(currentWallpaper)
    palette = color_thief.get_palette(color_count=20, quality=8)

    # White color on failure
    final = (228, 226, 226)
    # Looking for a big difference between 2 RGB values to decide
    # that the color has a tint that can be used
    for color in palette:
        dif1 = abs(color[0] - color[1])
        dif2 = abs(color[1] - color[2])
        dif3 = abs(color[0] - color[2])
        if dif1 > 70 or dif2 > 70 or dif3 > 70:
            # print(color)
            final = color
            break

    # Converting to the HSV color space and setting to 100% Saturation and 75% Value for the best colors for RGB
    hsv_col = colorsys.rgb_to_hsv(final[0] / 255, final[1] / 255, final[2] / 255)
    hsv_col = (hsv_col[0], 1, 0.75)

    # Convert back to RGB for LEDs
    final = colorsys.hsv_to_rgb(hsv_col[0], hsv_col[1], hsv_col[2])
    final = (int(final[0] * 255), int(final[1] * 255), int(final[2] * 255))

    return (final)

# Observer actions when the wallpaper changes
class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check that the wallpaper has changed
        currentWallpaper = getenv('APPDATA') + "\\Microsoft\\Windows\\Themes\\WallpaperEngineOverride.jpg"
        if event.src_path == currentWallpaper:
            # Take the color from wallpaper and set the lights for logitech and Govee
            final = take_color()
            logi_led.logi_led_set_lighting(final[0], final[1], final[2]) # Logitech

            loop = asyncio.new_event_loop() # Govee
            try:
                loop.run_until_complete(change_color(api_key, final, learning_storage))
            except:
                loop.close()


if __name__ == "__main__":
    # Govee api_key for your account
    api_key = "YOUR API KEY HERE"

    # Initializing a learning storage dummy
    learning_storage = LearningStorage()

    # Default location for the wallpaper on Windows
    currentWallpaper = getenv('APPDATA') + "\\Microsoft\\Windows\\Themes\\WallpaperEngineOverride.jpg"

    # Creating an observer to watch upates to the wallpaper copy
    observer = Observer()
    observer.schedule(Handler(), getenv('APPDATA') + "\\Microsoft\\Windows\\Themes")
    observer.start()

    # Wait a bit for the system to start on startup
    sleep(15)

    # Initialize the LEDs
    logi_led.logi_led_init()
    sleep(0.5)

    # Take the color on initial startup and set the led color for logitech mouse
    final = take_color()
    logi_led.logi_led_set_lighting(final[0], final[1], final[2]) # Logitech

    # An asyncio loop for the Govee lights
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(change_color(api_key, final, learning_storage))
    except:
        loop.close()

    # Folder observer interrupt when the wallpaper changes in the folder
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    # Start the observer
    observer.join()
