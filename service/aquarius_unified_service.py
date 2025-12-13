
from service.service_base import SMWinservice
from service.generic_watcher import GenericWatcher
from service.process_ocr import OCRProcessor
from service.process_fulltext import TextFileHandler
from service.process_import_pdf import ImportProcessorPDF
from service.process_import_csv import ImportProcessorCSV
from service.process_import_docid import ImportProcessorBarcodeDocID

import service.config_ocr as config_ocr
import service.config_fulltext_index as config_fulltext_index
import service.config_import_pdf as config_import_pdf
import service.config_import_csv as config_import_csv
import service.config_import as config_import

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
        
        processors = []

        # --- Sample processor definitions ---------------------------------

        # Uncomment any of the following blocks to enable a processor.

        # PDF Import Processor
        # processors.append(ImportProcessorPDF({
        #     "folder_to_watch": config_import_pdf.folder_to_watch,
        #     "process_existing_files": config_import_pdf.process_existing_files,
        #     "field_mappings": config_import_pdf.field_mappings,
        #     "document_type_id": config_import_pdf.document_type_id,
        #     "server": config_import_pdf.aquarius_api_url,
        #     "username": config_import_pdf.username,
        #     "password": config_import_pdf.password,
        # }))

        # CSV Import Processor
        # processors.append(ImportProcessorCSV({
        #     "folder_to_watch": config_import_csv.folder_to_watch,
        #     "process_existing_files": config_import_csv.process_existing_files,
        #     "document_type_id": config_import_csv.document_type_id,
        #     "field_mappings": config_import_csv.field_mappings,
        #     "pdf_index": config_import_csv.pdf_index,
        #     "server": config_import_csv.aquarius_api_url,
        #     "username": config_import_csv.username,
        #     "password": config_import_csv.password,
        # }))

        # Barcode DocID Import Processor
        # for folder, process_existing_files in config_import.folders_to_watch.items():
        #     processors.append(ImportProcessorBarcodeDocID({
        #         "folder_to_watch": folder,
        #         "process_existing_files": process_existing_files,
        #         "server": config_import.aquarius_api_url,
        #         "username": config_import.username,
        #         "password": config_import.password,
        #     }))

        # OCR Processor
        for folder, process_existing_files in config_ocr.folders_to_watch.items():
            processors.append(OCRProcessor({
                "folder_to_watch": folder,
                "process_existing_files": process_existing_files
            }))

        # Full Text Index Processor
        if config_fulltext_index.folder_solr_mapping:
            for folder_to_watch, mapping in config_fulltext_index.folder_solr_mapping.items():
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

