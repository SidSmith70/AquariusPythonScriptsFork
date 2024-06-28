
import os
from dotenv import load_dotenv
import utils.PDFSplitter as PDFSplitter
########################################################################################################################
# 
# Purpose: This script imports data into Aquarius DMS from a text file. The text file should contain the indexes for the
# documents to be imported. The text file should also contain the file paths for the documents to be imported.
#
########################################################################################################################

#******************* CONFIGURATION  ********************************************
from dotenv import load_dotenv
load_dotenv()
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL")  
doctypeCode = os.environ.get("DOCTYPEID")

FieldMap = {
            "Year": {"index": 0, "type": "text"},
            "Name":{"index": 3, "type": "text"},
            "PPIN": {"index": 2, "type": "text"},
            "Parcel Number":{"index": 1, "type": "text"},
            "Address":{"index": 4, "type": "text"},
}

#************************ CONFIGURATION ***********************************************************

import os
import sys
import utils.AquariusImaging as AquariusImaging
from datetime import datetime

#function for running a particular text file
def ProcessFile( file_path):
    
    # Read the text file
    try:
        print(f"{datetime.now()} Processing  {file_path}")  
        
        #initialize connection if necessary
        aqApi =  AquariusImaging.AquariusWebAPIWrapper(server)
        jsonhelper= AquariusImaging.AQJsonHelper(doctypeCode,FieldMap, None)

        if (aqApi.Authenticated == False):
            aqApi.authenticate(username,password)

        if (aqApi.Authenticated):

            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                documentCounter = 0
                pageCounter = 0
                docID = None

                #loop through the lines in the file
                for line in lines:
                            
                    indexValues = line.replace("\n","").split("|")
                    if (len(indexValues) == 1): #this is a filepath value, not indexes

                        #add page to document
                        response = aqApi.AddPageToDocument(docID, indexValues[0])
                        if (response.status_code==200):
                            print(f'{datetime.now()} Added page to document: {docID}')

                            #increment the page counter
                            pageCounter += 1

                        else:
                            print(f'{datetime.now()} Error adding page to document: {docID}')
                            
                            #raise an exception to stop processing the file
                            raise Exception(f'Error adding page to document: {docID} {response.status_code}')
                        

                    else:
                        
                        #create the document and get the docid
                        response = aqApi.CreateDocument(jsonhelper.new_document_JSON(indexValues))
                        if (response.status_code==200):
                            docID = response.json()
                        
                            print(f'{datetime.now()} Created new document: {docID}')   
                            
                            # add 1 to the document counter variable
                            documentCounter += 1

                            # split PDF file if necessary
                            pdffile = indexValues[len(indexValues) - 1]
                            pdfSplitter = PDFSplitter.PDFSplitter(pdffile, dpi=300, threshold=210)

                            # loop through the pages and add each one to the document.
                            for temp_path in pdfSplitter.get_temp_files():
                                response = aqApi.AddPageToDocument(docID, temp_path)
                                if (response.status_code==200):
                                    print(f'{datetime.now()} Added page to document: {docID}')

                                    #increment the page counter
                                    pageCounter += 1
                                else:
                                    print(f'{datetime.now()} Error adding page to document: {docID}')
                                    raise Exception(f'Error adding page to document: {docID} {response.status_code}')
                        else:
                            print(f'{datetime.now()} Error creating document: {response.status_code}')
                            raise Exception(f'Error creating document: {response.status_code}')

            #print to the console the number of documents and pages processed
            print(f'{datetime.now()} Processed {documentCounter} documents and {pageCounter} pages')                         
                    
    except Exception as e:
        print(f'{datetime.now()} Error processing file: {e}')
    finally:
        #delete the file
        print(f"{datetime.now()} Finished {file_path}")
        #os.remove(file_path)

ProcessFile("/home/sid/Downloads/data.txt")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            file_path = sys.argv[i]
            if os.path.isfile(file_path):
                ProcessFile(file_path)