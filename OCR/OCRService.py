import time
from ServiceBase import SMWinservice
from OCRFullTextWatcher import OCRFullTextWatcher  # Fixed import statement

class OCRService(SMWinservice):
    _svc_name_ = "OCRService"
    _svc_display_name_ = "OCR Service"
    _svc_description_ = "Aquarius OCR Service"

    def start(self):
        self.isrunning = True
        self.watcher = OCRFullTextWatcher()  # Initialize the watcher here

    def main(self):
        self.watcher.start()
        self.watcher.run()

    def stop(self):
        self.isrunning = False
        self.watcher.stop()  # Properly stop the watcher

if __name__ == '__main__':
    OCRService.parse_command_line()
