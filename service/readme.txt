
OCR Requires Tesseract ocr installed on the machine and added to the path.
Full text processing requires solr server.



Install the Service: Run the following command:

python -m path.to.module.AquariusFileWatcherService install


Start the Service: After installing, you can start the service using:

python -m path.to.module.AquariusFileWatcherService start



Stop the Service: If you need to stop the service, use:

python -m path.to.module.AquariusFileWatcherService stop


Uninstall the Service: If you want to uninstall the service, use:

python -m path.to.module.AquariusFileWatcherService remove


Scripts must be run as modules for relative imports to work properly. So rather than running generic_watcher.py, 
you'll need to run as a module service.generic_watcher. Like so:
 
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Module",
            "type": "debugpy",
            "request": "launch",
            "module": "service.generic_watcher"
        }
    ]
}