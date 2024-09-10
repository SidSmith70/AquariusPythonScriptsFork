
from service_base import SMWinservice
from generic_watcher import GenericWatcher
from service.ocr_processor import OCRProcessor
import service.config_ocr as config_ocr


#******************* LOAD THE CONFIGURATION FILE ********************************************
from dotenv import load_dotenv
load_dotenv()
#************************ CONFIGURATION ***********************************************************

class AquariusFileWatcherService(SMWinservice):
    _svc_name_ = "AquariusOCRService"
    _svc_display_name_ = "Aquarius OCR Service"
    _svc_description_ = "Aquarius OCR Service"

    def start(self):
        
        self.isrunning = True
        
        processors=[]

        for folder, process_existing_files in config_ocr.folders_to_watch.items():
        # Create a processor instance and inject the folder and flag into the handler.
            processors.append(OCRProcessor({
                "folder_to_watch": folder,
                "process_existing_files": process_existing_files
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

