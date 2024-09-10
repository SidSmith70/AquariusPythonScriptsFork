import time
from service.service_base import SMWinservice
from service.generic_watcher import GenericWatcher
from service.process_import_docid import ImportProcessorBarcodeDocID
from service.config_import import config_import 

class AquariusFileWatcherService(SMWinservice):
    _svc_name_ = "AquariusImportService"
    _svc_display_name_ = "Aquarius Import Service"
    _svc_description_ = "Aquarius Import Service"

    def start(self):
        
        self.isrunning = True
        
        processors=[]

        for folder, process_existing_files in config_import.folders_to_watch.items():
        # Create a processor instance and inject the folder and flag into the handler.
            processors.append(ImportProcessorBarcodeDocID({
                "folder_to_watch": folder,
                "process_existing_files": process_existing_files,
                "server": config_import.aquarius_api_url,
                "username": config_import.username,
                "password": config_import.password
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

