
########################################################################################################################
# 
# Purpose: This script watches for new tif, jpg files and runs tesseract OCR on them.  
#          It also watches for new text files, and sends them to solr.
#
########################################################################################################################

from watchdog.observers import Observer
from FullTextHandler import TextFileHandler
import time


#******************* LOAD THE CONFIGURATION FILE ********************************************
import config
#************************ CONFIGURATION ***********************************************************


class FullTextWatcher:
    def __init__(self):
        self.running = True
        self.observer = Observer()
        self.image_handlers = []
        self.text_handlers = []

    def start(self):

        # Create a handler instance for each folder_solr_mapping
        for folder_to_watch, mapping in config.folder_solr_mapping.items():

            print(f"Watching folder: {folder_to_watch}")

            solrUrl = mapping["solrUrl"]
            path_replacement_pairs = mapping["path_replacement_pairs"]

            # Create a TextHandler instance to handle the text files.
            text_handler = TextFileHandler(folder_to_watch,solrUrl, path_replacement_pairs)
            self.text_handlers.append(text_handler)
            
            self.observer.schedule(text_handler, folder_to_watch, recursive=True)

        self.observer.start()

        # Optionally, process all existing files in the folder tree:
               
        if config.process_existing_text_files:
            for text_handler in self.text_handlers:
                text_handler.ProcessALL()

    def stop(self):

        self.running = False
                  
        for text_handler in self.text_handlers:
            text_handler.stop()
            

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
    watcher = FullTextWatcher()
    watcher.start()
    try:
        watcher.run()

    except KeyboardInterrupt:
        watcher.stop()
       

