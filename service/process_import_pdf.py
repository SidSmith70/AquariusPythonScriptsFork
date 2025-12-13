############################################################################################################
# This script is used to import files into Aquarius Imaging using the Aquarius Imaging API.
# 
# ############################################################################################################

from datetime import datetime
import tempfile
import os
from PyPDF2 import PdfReader, PdfWriter

import utils.AquariusImaging as AquariusImaging

# This class handles importing files.
class ImportProcessorPDF():
    
    def __init__(self, config):

        self.config = config
        
        # Authenticate to Aquarius Imaging
        self.aqApi =  AquariusImaging.AquariusWebAPIWrapper(config['server'])                     
        self.aqApi.authenticate(config['username'], config['password'])

        # Get the query definition for the document type, and create a JSON helper class to help us build the JSON for the API calls
        if (self.aqApi.Authenticated):
            pass
        else:
            raise Exception(f'{datetime.now()} Error authenticating to Aquarius Imaging')

    def Process(self, file_path):
        try:
            if file_path.lower().endswith('.pdf'):
                print(f"{datetime.now()} Processing {file_path}")
                
                temp_files = []

                # Create a temp dir to hold the single-page PDFs
                with tempfile.TemporaryDirectory() as temp_dir:

                    # Get the metadata from the file path
                    metadata = self.get_metadata_from_path(file_path)

                    # todo: create a document and get the doc_id
                    #create json for new document
                    newDocumentJson = {
                        "application": None,
                        "doctype": self.config['document_type_id'],
                        "pages": [],
                        "docID": None,
                        "indexData": metadata
                    }

                    # Open the source PDF
                    reader = PdfReader(file_path)
                    
                    # Iterate pages
                    for i, page in enumerate(reader.pages):
                        writer = PdfWriter()
                        writer.add_page(page)

                        # Build output filename
                        output_file = os.path.join(temp_dir, f"page_{i}.pdf")
                        with open(output_file, "wb") as out_f:
                            writer.write(out_f)

                        print(f"{datetime.now()} → Prepared {output_file} for new document")
                        temp_files.append(output_file)
                    
                    
                    #create the document and get the docid
                    response = self.aqApi.CreateDocument(newDocumentJson)
                    if (response.status_code) == 200:
                        docid = response.json()

                        print(docid)

                        # Bulk-upload the single-page PDFs
                        response = self.aqApi.AddPagesToDocument(docid, temp_files)
                        if response.status_code != 200:
                            raise Exception(f"Error uploading PDF pages: {response.status_code} {response.text}")

                        #if we made it here, the upload was successful, so we can now delete the incoming file
                        os.remove(file_path)
                        print(f"{datetime.now()} → Deleted {file_path} after successful upload")
                
                # TemporaryDirectory and all files inside are auto-deleted here
                        
                    
        except Exception as ex:
            print(f'{datetime.now()} Error: {ex.args[0]}')

    
    def get_metadata_from_path(self, file_path):
        # Split the path into parts
        path_parts = file_path.split(os.sep)
        metadata = []

        for field, index in self.config['field_mappings'].items():
            if index >= len(path_parts):
                raise Exception(f"Index {index} out of range for path parts: {path_parts}")

            part = path_parts[index]

            # if this is the last element (the filename), strip its extension
            if index == len(path_parts) - 1:
                part = os.path.splitext(part)[0]   # returns (name, ext)

            element = {
                "fieldName": field,
                "value": part
            }
           
            #add this element to the metadata so that it creates a list of indexdata values like this: "indexData": [
            #         {
            #             "fieldName": "Employee Name",
            #             "value": "Nelson"
            #         }
            #     ]
            metadata.append(element)



            # newDocumentJson = {
            #     "application": None,
            #     "doctype": doctypeID,
            #     "pages": [],
            #     "docID": None,
            #     "indexData": [
            #         {
            #             "fieldName": "Employee Name",
            #             "value": "Nelson"
            #         }
            #     ]
            # }
        return metadata
    

  