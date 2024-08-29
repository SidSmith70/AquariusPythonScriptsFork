import time
from ServiceBase import SMWinservice
from OCRWatcher import OCRWatcher
from FullTextWatcher import FullTextWatcher
from OCRFullTextWatcher import OCRFullTextWatcher  
from UnifiedWatcher import UnifiedWatcher

class AquariusFileWatcherService(SMWinservice):
    _svc_name_ = "AquariusFileWatcherService"
    _svc_display_name_ = "Aquarius FileWatcher Service"
    _svc_description_ = "Aquarius FileWatcher Service"

    def start(self):
        self.isrunning = True
        self.watcher = UnifiedWatcher()  # self.get_watcher(watcher_type) # OCRFullTextWatcher()  # Initialize the watcher here

    def main(self):
        self.watcher.start()
        self.watcher.run()

    def stop(self):
        self.isrunning = False
        self.watcher.stop()  # Properly stop the watcher
   

if __name__ == '__main__':
    AquariusFileWatcherService.parse_command_line()
