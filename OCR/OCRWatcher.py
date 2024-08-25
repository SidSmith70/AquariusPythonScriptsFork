
########################################################################################################################
# 
# Purpose: This script watches for new tif, jpg files and runs tesseract OCR on them.  
#          It also watches for new text files, and sends them to solr.
#
########################################################################################################################

from watchdog.observers import Observer
from OCRHandler import ImageFileHandler
import time

#******************* LOAD THE CONFIGURATION FILE ********************************************
import config
#************************ CONFIGURATION ***********************************************************


class OCRWatcher:
    def __init__(self):
        self.running = True
        self.observer = Observer()
        self.image_handlers = []
        self.text_handlers = []

    def start(self):

        # Create a handler instance for each folder_solr_mapping
        for folder_to_watch, mapping in config.folder_solr_mapping.items():

            print(f"Watching folder: {folder_to_watch}")
       
            # Create a MyHandler instance to handle the image files.
            image_handler = ImageFileHandler(folder_to_watch)
            self.image_handlers.append(image_handler)
            
            self.observer.schedule(image_handler, folder_to_watch, recursive=True)
            
        self.observer.start()

        # Optionally, process all existing files in the folder tree:
        if config.process_existing_image_files:
            for image_handler in self.image_handlers:
                image_handler.ProcessALL()
        
        if config.process_existing_text_files:
            for text_handler in self.text_handlers:
                text_handler.ProcessALL()

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
    watcher = OCRWatcher()
    watcher.start()
    try:
        watcher.run()

    except KeyboardInterrupt:
        watcher.stop()
       

