# Moves downloaded images and files to Desktop and deletes after 24 hours
# By Jeet Vinaychandra Tevani (19/03/24)
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from send2trash import send2trash

import os
import time
import logging

source_dir = "/Users/jeettevani/Downloads"
dest_dir = "/Users/jeettevani/Desktop"

hours_in_seconds = 86400

usual_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", 
                    ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", 
                    ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", 
                    ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", 
                    ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", 
                    ".ico", ".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", 
                    ".ppt", ".pptx"]

# Deletes usual_extensions files on Desktop after 24 hours
def fileTimeExisted(name):
    destination = dest_dir + "/" + name
    creationTime = os.path.getctime(destination)
    currentTimeSinceEpoch = time.time()
    actualCurrentTime = currentTimeSinceEpoch - creationTime
    for i in usual_extensions:
        if name.endswith(i) or name.endswith(i.upper()):
            if (actualCurrentTime > 1):
                send2trash(destination)  

# Moves files from source directory (Downloads) to destination
# directory (Desktop)
def fileMoving(name):
    for i in usual_extensions:
        if name.endswith(i) or name.endswith(i.upper()):
            starting = source_dir + "/" + name
            destination = dest_dir + "/" + name
            Path(starting).rename(destination)

# Keeps track of all movement in the source directory
class movingDirectories(LoggingEventHandler):
     def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                fileMoving(name)

# Executes the program
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    logging.info(f'start watching directory {path!r}')
    event_handler = movingDirectories()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
            # Runs throughout the program regardless of
            # what occurs in the source directory
            with os.scandir(dest_dir) as entries:
                for entry in entries:
                    name = entry.name
                    fileTimeExisted(name)
    except KeyboardInterrupt:
       observer.stop()
       observer.join()
