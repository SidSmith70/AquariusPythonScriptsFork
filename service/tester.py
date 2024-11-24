########################################################################################################################
# 
# Purpose: This class represents an observer, which accepts a list of injected processors. Each processor creates a handler 
# to watch for file system events in the specified folder. Each handler will call it's processor to process files as 
# they are created in the watched folder. The observer will start the handlers and run them in separate threads.
#
########################################################################################################################

from service.process_ocr import OCRProcessor
from service.process_import_docid import ImportProcessorBarcodeDocID
from service.generic_watcher import GenericWatcher
import service.config_ocr as config_ocr
import service.config_import as config_import
import os



if __name__ == "__main__":
    
    # create a processor instance to handle the image files, and inject it into the handler.
    
    processors=[]

    for folder, process_existing_files in config_ocr.folders_to_watch.items():
        # Create a processor instance and inject the folder and flag into the handler.
            processors.append(OCRProcessor({
                "folder_to_watch": folder,
                "process_existing_files": process_existing_files
            }))

    # for folder, process_existing_files in config_import.folders_to_watch.items():
    #     # Create a processor instance and inject the folder and flag into the handler.
    #         processors.append(ImportProcessorBarcodeDocID({
    #             "folder_to_watch": folder,
    #             "process_existing_files": process_existing_files,
    #             "server": config_import.aquarius_api_url,
    #             "username": config_import.username,
    #             "password": config_import.password
    #         }))


    watcher = GenericWatcher(processors)

    watcher.start()

    try:
        watcher.run()

    except KeyboardInterrupt:
        watcher.stop()
       
