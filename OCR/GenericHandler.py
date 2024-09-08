
from watchdog.events import FileSystemEventHandler
from PIL import Image
from datetime import datetime
import os
import time


# This class handles the file system events for the folder being watched
class FileHandler(FileSystemEventHandler):

    def __init__(self, folder_to_watch, processor ):
        super().__init__()
        self.folder_to_watch = folder_to_watch
        self.running = True
        self.processor = processor
    
    def on_created(self, event):
        try:
            if not event.is_directory:
                file_path = event.src_path

                # wait for the file to be fully written
                file_size = -1
                while os.path.getsize(file_path) != file_size:
                    
                    file_size = os.path.getsize(file_path)
                    time.sleep(5) # wait for 5 seconds
                
                self.processor.Process(file_path)

        except Exception as ex:
            print(f'{datetime.now()} Error: {str(ex)}')
      
    

    def ProcessALL(self):
        try:
            # To process all files in the folder:
            folder_to_process = self.folder_to_watch  # Assuming you pass the folder path when creating the handler instance

            for root, _, files in os.walk(folder_to_process):
                    for filename in files:
                                                
                        self.processor.Process(os.path.join(root,filename))

        except Exception as ex:
            print(f'{datetime.now()} Error: {str(ex)}')
            

    def stop(self):
        self.running = False
