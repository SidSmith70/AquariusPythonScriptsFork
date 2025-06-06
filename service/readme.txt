
OCR Requires the Tesseract OCR engine installed on the machine and added to the
PATH. On Windows you can download it from https://github.com/UB-Mannheim/tesse
ract/wiki.
Full text processing requires a Solr server.

Windows installations may also require the Microsoft Visual C++ Redistributable
for some packages (e.g., opencv-python). After installing dependencies, run
`pywin32_postinstall.py -install` from the Python Scripts directory if prompted.

Each processor has its own requirements file. Install only what you need using
`pip install -r <file>`:

```
requirements_base.txt      # Generic watcher/service support
requirements_pdf.txt       # PDF import processor
requirements_csv.txt       # CSV import processor
requirements_docid.txt     # Barcode DocID processor
requirements_ocr.txt       # OCR processor
requirements_fulltext.txt  # Full text indexing
```



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