
from service.service_base import SMWinservice
from service.generic_watcher import GenericWatcher
from service.process_ocr import OCRProcessor
from service.process_fulltext import TextFileHandler
import service.config_ocr as config_ocr
import service.config_fulltext_index as config_fulltext_index

#******************* LOAD THE CONFIGURATION FILE ********************************************
from dotenv import load_dotenv
load_dotenv()
#************************ CONFIGURATION ***********************************************************

class AquariusFileWatcherService(SMWinservice):
    _svc_name_ = "AquariusUnifiedService"
    _svc_display_name_ = "Aquarius Unified Service"
    _svc_description_ = "Aquarius Unified Service"

    def start(self):
        
        self.isrunning = True
        
        processors=[]

        for folder, process_existing_files in config_ocr.folders_to_watch.items():
        # Create a processor instance and inject the folder and flag into the handler.
            processors.append(OCRProcessor({
                "folder_to_watch": folder,
                "process_existing_files": process_existing_files
            }))

        if config_fulltext_index.folder_solr_mapping:
            for folder_to_watch, mapping in config_fulltext_index.folder_solr_mapping.items():

                print(f"Watching folder: {folder_to_watch}")
                                               
                solrUrl = mapping["solrUrl"]
                path_replacement_pairs = mapping["path_replacement_pairs"]
                
                processors.append(TextFileHandler({
                    "folder_to_watch": folder_to_watch,
                    "solrUrl": solrUrl,
                    "path_replacement_pairs": path_replacement_pairs
                }))
                

        self.watcher = GenericWatcher(processors)
        
    def main(self):
        self.watcher.start()
        self.watcher.run()

    def stop(self):
        self.isrunning = False
        self.watcher.stop()  # Properly stop the watcher
   

if __name__ == '__main__':
    AquariusFileWatcherService.parse_command_line()

