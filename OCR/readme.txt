
OCR Requires Tesseract ocr installed on the machine and added to the path.
Full text processing requires solr server.



Install the Service: Run the following command:

python AquariusFileWatcherService.py install

Start the Service: After installing, you can start the service using:

python AquariusFileWatcherService.py start


Stop the Service: If you need to stop the service, use:

python AquariusFileWatcherService.py stop


Uninstall the Service: If you want to uninstall the service, use:

python AquariusFileWatcherService.py remove


Scripts must be run as modules for relative imports to work properly. So rather than running generic_watcher.py, 
you'll need to run as a module OCR.generic_watcher. Like so:
 
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Module",
            "type": "debugpy",
            "request": "launch",
            "module": "OCR.generic_watcher"
        }
    ]
}