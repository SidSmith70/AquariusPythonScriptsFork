########################################################################################################################
# 
# Purpose: This class represents an observer, which accepts a list of injected processors. Each processor creates a handler 
# to watch for file system events in the specified folder. Each handler will call it's processor to process files as 
# they are created in the watched folder. The observer will start the handlers and run them in separate threads.
#
########################################################################################################################

from service.ocr_processor import OCRProcessor
from service.import_processor_docid import ImportProcessorBarcodeDocID
from service.generic_watcher import GenericWatcher
import os



if __name__ == "__main__":
    
    # create a processor instance to handle the image files, and inject it into the handler.
    processor_config = {
        "server": os.environ.get("AQUARIUSAPIURL") ,
        "username": os.environ.get("USERNAME"),
        "password": os.environ.get("PASSWORD"),
        "folder_to_watch": './service/WatchedFolder',
        "process_existing_files": True,
    }

    processors=[]

    processors.append(ImportProcessorBarcodeDocID(processor_config))

    watcher = GenericWatcher(processors)

    watcher.start()

    try:
        watcher.run()

    except KeyboardInterrupt:
        watcher.stop()
       

