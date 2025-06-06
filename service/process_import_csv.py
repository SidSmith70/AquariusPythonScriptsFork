"""
Process CSV files to create documents in Aquarius Imaging.
Each CSV row should have fields for index data followed by the
path to a PDF file to upload. Field mappings determine which
column values map to document index fields.
"""

from datetime import datetime
import tempfile
import os
import csv
from PyPDF2 import PdfReader, PdfWriter

import utils.AquariusImaging as AquariusImaging

class ImportProcessorCSV:
    def __init__(self, config):
        self.config = config
        self.aqApi = AquariusImaging.AquariusWebAPIWrapper(config['server'])
        self.aqApi.authenticate(config['username'], config['password'])
        if not self.aqApi.Authenticated:
            raise Exception(f"{datetime.now()} Error authenticating to Aquarius Imaging")

    def Process(self, file_path):
        try:
            if file_path.lower().endswith('.csv'):
                print(f"{datetime.now()} Processing {file_path}")
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if not row:
                            continue
                        try:
                            metadata = self.get_metadata_from_row(row)
                            pdf_path = row[self.config['pdf_index']]
                            self._process_pdf(pdf_path, metadata)
                        except Exception as row_ex:
                            print(f"{datetime.now()} Error processing row {row}: {row_ex}")
                os.remove(file_path)
                print(f"{datetime.now()} → Deleted {file_path} after successful processing")
        except Exception as ex:
            print(f"{datetime.now()} Error: {ex}")

    def _process_pdf(self, pdf_path, metadata):
        temp_files = []
        with tempfile.TemporaryDirectory() as temp_dir:
            reader = PdfReader(pdf_path)
            for i, page in enumerate(reader.pages):
                writer = PdfWriter()
                writer.add_page(page)
                output_file = os.path.join(temp_dir, f"page_{i}.pdf")
                with open(output_file, 'wb') as out_f:
                    writer.write(out_f)
                temp_files.append(output_file)
            new_document = {
                "application": None,
                "doctype": self.config['document_type_id'],
                "pages": [],
                "docID": None,
                "indexData": metadata
            }
            response = self.aqApi.CreateDocument(new_document)
            if response.status_code == 200:
                docid = response.json()
                upload_response = self.aqApi.AddPagesToDocument(docid, temp_files)
                if upload_response.status_code != 200:
                    raise Exception(f"Error uploading PDF pages: {upload_response.status_code} {upload_response.text}")
                os.remove(pdf_path)
                print(f"{datetime.now()} → Deleted {pdf_path} after successful upload")
            else:
                raise Exception(f"Error creating document: {response.status_code} {response.text}")

    def get_metadata_from_row(self, row):
        metadata = []
        for field, index in self.config['field_mappings'].items():
            if index >= len(row):
                raise Exception(f"Index {index} out of range for row: {row}")
            metadata.append({"fieldName": field, "value": row[index]})
        return metadata
