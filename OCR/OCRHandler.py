
from watchdog.events import FileSystemEventHandler
import pytesseract
from PIL import Image
from datetime import datetime

import os
import time


# This class handles the file system events for the folder being watched
class ImageFileHandler(FileSystemEventHandler):

    def __init__(self, folder_to_watch ):
        super().__init__()
        self.folder_to_watch = folder_to_watch
        self.running = True

    def on_created(self, event):
        try:
            if not event.is_directory and (event.src_path.lower().endswith('.tif') or event.src_path.lower().endswith('.jpg') ):
                file_path = event.src_path

                # wait for the file to be fully written
                file_size = -1
                while os.path.getsize(file_path) != file_size:
                    file_size = os.path.getsize(file_path)
                    time.sleep(5) # wait for 5 seconds
                self.ProcessOCR(file_path)

        except Exception as ex:
            print(f'{datetime.now()} Error: {str(ex)}')

        
    def ProcessOCR(self, file_path):

       #run the tessaract OCR process
        try:
            print(f"{datetime.now()} Processing  {file_path}")
            
            img = Image.open(file_path)

            #run the ocr
            config='-c preserve_interword_spaces=1 --oem {} --psm {} -l {}'.format('3','1','eng+spa')
            ocr_text = pytesseract.image_to_string(img, config=config).strip()


            #save the text file
            textkey = file_path[0:-4] + '.txt'
            with open(textkey, 'w') as f:
                f.write(ocr_text)
                print(f"{datetime.now()} Saved text file {textkey}")

        except Exception as ex:
            print(f'{datetime.now()} Error: {ex.args[0]}')

    def ProcessALL(self):
        try:
            # To process all files in the folder:
            folder_to_process = self.folder_to_watch  # Assuming you pass the folder path when creating the handler instance

            for root, _, files in os.walk(folder_to_process):
                    for filename in files:
                        
                        if filename.lower().endswith('.tif') or filename.lower().endswith('.jpg'):
                            text_file_path = os.path.join(root, os.path.splitext(filename)[0] + '.txt')
                            #print(text_file_path)
                            # Check if the text file already exists.
                            if not self.running:
                                break
                            elif not os.path.exists(text_file_path):

                                self.ProcessOCR(os.path.join(root,filename))

        except Exception as ex:
            print(f'{datetime.now()} Error: {str(ex)}')
            

    def stop(self):
        self.running = False
