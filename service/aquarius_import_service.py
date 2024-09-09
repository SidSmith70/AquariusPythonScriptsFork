import time
from service_base import SMWinservice
from generic_watcher import GenericWatcher
from import_processor_docid import ImportProcessorBarcodeDocID
import os
import os


#******************* LOAD THE CONFIGURATION FILE ********************************************
from dotenv import load_dotenv
load_dotenv()
#************************ CONFIGURATION ***********************************************************

class AquariusFileWatcherService(SMWinservice):
    _svc_name_ = "AquariusImportService"
    _svc_display_name_ = "Aquarius Import Service"
    _svc_description_ = "Aquarius Import Service"

    def start(self):
        
        self.isrunning = True
        
         # create a processor instance to handle the image files, and inject it into the handler.
        importconfig = {
            "server": os.environ.get("AQUARIUSAPIURL") ,
            "username": os.environ.get("USERNAME"),
            "password": os.environ.get("PASSWORD"),
            "folder_to_watch": './OCR/WatchedFolder',
            "process_existing_files": True,
        }

        processors=[]

        processors.append(ImportProcessorBarcodeDocID(importconfig))

        self.watcher = GenericWatcher(processors)  

    def main(self):
        self.watcher.start()
        self.watcher.run()

    def stop(self):
        self.isrunning = False
        self.watcher.stop()  # Properly stop the watcher
   

if __name__ == '__main__':
    AquariusFileWatcherService.parse_command_line()

