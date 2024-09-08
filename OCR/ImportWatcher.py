
########################################################################################################################
# 
# Purpose: This script watches for new tif, jpg files and processes them 
#
########################################################################################################################

from watchdog.observers import Observer
from GenericHandler import FileHandler
from ImportProcessor import ImportProcessor
import time
import os
import dotenv

#******************* LOAD THE CONFIGURATION FILE ********************************************
from dotenv import load_dotenv
load_dotenv()
#************************ CONFIGURATION ***********************************************************

class ImportWatcher:
    def __init__(self):
        self.running = True
        self.observer = Observer()
        self.image_handlers = []
        

    def start(self):

        # Create a handler instance for each folder to watch
        #if config.watcher_type == "OCRWatcher" or config.watcher_type == "OCRFullTextWatcher":
        folder_to_watch = './OCR/WatchedFolder'
        process_existing_image_files = False

        print(f"Watching folder: {folder_to_watch}")
    
        # create a processor instance to handle the image files, and inject it into the handler.
        importconfig = {
            "server": os.environ.get("AQUARIUSAPIURL") ,
            "username": os.environ.get("USERNAME"),
            "password": os.environ.get("PASSWORD"),
        }

        processor =  ImportProcessor(importconfig)
        image_handler =  FileHandler(folder_to_watch, processor)

        # schedule the handler to watch the folder
        self.image_handlers.append(image_handler)
        self.observer.schedule(image_handler, folder_to_watch, recursive=True)
            
        self.observer.start()

        # Optionally, process all existing files in the folder tree:
        if process_existing_image_files:
            for image_handler in self.image_handlers:
                image_handler.ProcessALL()
        

    def stop(self):

        self.running = False
        for image_handler in self.image_handlers:
            image_handler.stop()
           
        self.observer.stop()
        self.observer.join()


    def run(self):

        # go into an infinite loop.  The observer will run in a separate thread.
        try:
            while self.running:
                time.sleep(5)

        finally:
            self.stop()



if __name__ == "__main__":
    watcher = ImportWatcher()
    watcher.start()
    try:
        watcher.run()

    except KeyboardInterrupt:
        watcher.stop()
       

