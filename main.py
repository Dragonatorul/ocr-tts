# This is a sample Python script.

import cv2 as cv
import cv2
import pytesseract
import win32com.client
import yaml
import os
import logging
import time

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.WARNING,
    filemode='a',
    filename="ocr-tts.log",
    encoding='utf-8')

## Define template_file as global variable to be able to use it in the event handler.
template_file = ""


def read(reference_file):
    # reference_file = "test_data/Stray Screenshot 2022.07.23 - 21.37.00.44.png"
    # reference_file = "test_data/Stray Screenshot 2022.07.23 - 21.35.27.60.png"
    # # reference_file = "test_data/Stray Screenshot 2022.07.23 - 21.37.00.44_resize.png"
    # reference_file = "test_data/Stray Screenshot 2022.07.23 - 21.35.19.12.png"
    # template_file = "test_data/TEMPLATE_1.png"

    global template_file

    ## Match the pattern of the text box to the given image
    logging.debug(template_file)
    logging.debug(reference_file)
    # print(reference_file)
    img = cv2.imread(reference_file, 0)
    ## ! Screenshot creation triggers three events: Created, modified, modified. Loading the image in the first two
    ## ! cases result in a None type object. Probably the file is not saved yet. Need to skip when this happens and
    ## ! wait for the event where the file is completely saved.
    if img is None:
        return
    img2 = img.copy()
    template = cv2.imread(template_file, 0)
    w, h = template.shape[::-1]

    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    ## ! Chose a method that seems to be working OK.
    meth = methods[1]
    img = img2.copy()
    method = eval(meth)
    ## Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    ## If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    x1 = top_left[0]
    y1 = top_left[1]

    x2 = bottom_right[0]
    y2 = bottom_right[1]

    ## Crop the image to the identified text box
    crop = img[y1:y2, x1:x2]

    ## Get the text from the cropped text box
    img_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    print(text)
    logging.debug(f"Detected text: \n{text}")

    ## Speak the text using the Windows TTS service
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


def on_created(event):
    logging.debug(f"File created: {event.src_path}")


def on_deleted(event):
    logging.debug(f"File deleted: {event.src_path}")


def on_modified(event):
    logging.debug(f"File modified: {event.src_path}")
    read(reference_file=event.src_path)


def on_moved(event):
    logging.debug(f"File moved from {event.src_path} to {event.dest_path}")


def crash(msg):
    print(msg)
    logging.critical(msg)
    exit(1)


def config_error(msg):
    crash(msg)


def run():
    settings_file = "settings.yaml"
    logging.debug(f"Opening settings file {settings_file}")
    if os.path.isfile(settings_file):
        with open(settings_file, "rb") as f:
            settings = yaml.safe_load(f)
    else:
        msg = "ERROR: Could not find 'settings.yaml' file. Please see README for configuration instructions. \n\n" \
              "EXITING SCRIPT!"
        config_error(msg)

    watch_location = settings['watch_location']
    logging.debug(f"Testing location {watch_location}")
    if not os.path.isdir(watch_location):
        msg = f"ERROR: Could not find screenshot folder at location {watch_location} \n" \
              f"Please see README for configuration instructions. \n\n" \
              f"EXITING SCRIPT!"
        config_error(msg)

    global template_file
    template_file = settings['template_file']
    logging.debug(f"Testing location {template_file}")
    if not os.path.isfile(template_file):
        msg = f"ERROR: Could not find template file at location {template_file} \n" \
              f"Please see README for configuration instructions. \n\n" \
              f"EXITING SCRIPT!"
        config_error(msg)

    patterns = ["*.png", "*.jpg", "*.jpeg"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = False
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    # Define event handlers
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved

    # Create the Observer
    path = watch_location
    go_recursively = False
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    # Start the observer and monitor the folder
    logging.debug(f"Starting observer for location {path}")
    print("Waiting for screenshots.")
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


if __name__ == '__main__':
    logging.debug(f"Starting script.")
    run()
