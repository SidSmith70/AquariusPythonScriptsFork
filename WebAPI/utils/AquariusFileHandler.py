import utils.AquariusImaging as AquariusImaging
import tempfile
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os
import time
import cv2

class AquariusFileHandler(FileSystemEventHandler):
   
    def __init__(self, doctypeCode,fieldMap,server,username,password, appendExistingDocuments,filter, data_extractor_function, extensions_to_watch = ['.tif', '.jpg', '.jpeg','.pdf', '.png']):
        super().__init__()

        self.appendExistingDocuments = appendExistingDocuments
        self.filter = filter
        self.extract_data = data_extractor_function
        self.appendExistingDocuments = appendExistingDocuments
        self.extensions_to_watch = extensions_to_watch  # ['.tif', '.jpg', '.jpeg','.pdf', '.png']  # Example extensions

        # Authenticate to Aquarius Imaging
        self.aqApi =  AquariusImaging.AquariusWebAPIWrapper(server)                     
        self.aqApi.authenticate(username,password)

        # Get the query definition for the document type, and create a JSON helper class to help us build the JSON for the API calls
        if (self.aqApi.Authenticated):
            response = self.aqApi.GetQueryDefinition(doctypeCode)
                            
            if (response.status_code==200):
                qd = response.json()
                               
                self.JSONHelper = AquariusImaging.AQJsonHelper(doctypeCode,fieldMap,qd)
            else:
                
                raise Exception(f'{datetime.now()} Error getting query definition for {doctypeCode}: {response.status_code} {response.text}')
        else:
           
            raise Exception(f'{datetime.now()} Error authenticating to Aquarius Imaging')
              


    def checkFilter(self, indexValues):
        #check the filter to see if we should process this document

        if (self.filter == ""): return True
        else:
            filterArray = self.filter.split(" ")

            filterField = filterArray[0]
            filterOperator = filterArray[1]
            filterValue = filterArray[2]

            # check the indexValues field to see if we should process this document
            if filterOperator == "=":
                if (indexValues[self.JSONHelper.fieldMap[filterField]] == filterValue):
                    return True
                else: return False
            else:
            
                if (indexValues[self.JSONHelper.fieldMap[filterField]] != filterValue):
                    return True
                else: return False


    def on_created(self, event):
        try:
            if not event.is_directory:
                file_extension = os.path.splitext(event.src_path.lower())[1]
                if file_extension in self.extensions_to_watch:
                    file_path = event.src_path
                    file_size = -1
                    while os.path.getsize(file_path) != file_size:
                        file_size = os.path.getsize(file_path)
                        time.sleep(5) # wait for 5 seconds
                    self.ProcessFile(file_path)
        except Exception as ex:
            print(f'{datetime.now()} Error: {str(ex)}')

    def ProcessFile(self, file_path):

        # Extract metadata from file.
        try:
            print(f"{datetime.now()} Processing  {file_path}")
            indexValues =  self.extract_data(file_path)
        
            if indexValues:
                #print(f'{datetime.now()} QR Code Value: {qr_code_value}')

                #indexValues = qr_code_value.split("|")
               
                if(self.checkFilter(indexValues) == True):
                                   
                    if (self.aqApi.Authenticated):

                        docID = None
                        queryResults = []

                        #if we're appending documents, attempt to look up this document.
                        if (self.appendExistingDocuments == True):
                        
                            #run the query
                            response = self.aqApi.RunQuery(self.JSONHelper.query_JSON(indexValues))
                            if (response.status_code==200):
                                queryResults = response.json()

                            if(len(queryResults) > 0):
                                #if document was found, use the docid of the first one
                                docID = queryResults[0]["docID"]
                                print(f'{datetime.now()} Document Found: {docID}') 

                        #if a document was NOT found, create one
                        if (docID == None):
                            #create the document and get the docid
                            response = self.aqApi.CreateDocument(self.JSONHelper.new_document_JSON(indexValues))
                            if (response.status_code==200):
                                docID = response.json()
                            
                            print(f'{datetime.now()} Created new document: {docID}') 

                        # if this is a tif file, we need to split it into single page tiffs
                        # and upload each page individually.
                        if (file_path.lower().endswith('.tif')):                    
                            temp_files = []
                            # Create a temporary directory to store the single-page TIFF files.
                            # When we exit this scope, the files are automatically deleted.
                            with tempfile.TemporaryDirectory() as temp_dir:
                            
                                # Open the multipage TIFF file
                                tiff_file = []

                                #tiff_file = cv2.imread(file_path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_ANYCOLOR)
                                retbool, tiff_file = cv2.imreadmulti(mats=tiff_file,
                                                            filename=file_path,
                                                            flags=cv2.IMREAD_ANYCOLOR)
                                
                                # Iterate over each page in the TIFF file
                                if len(tiff_file) > 0:
                                    for i in range(len(tiff_file)):
                                        
                                        #skip the QR Code page if we're adding to an existing document.
                                        if not(len(queryResults) > 0 and i==0):
                                                                                    
                                            # Create a filename for the single-page TIFF file
                                            output_file = os.path.join(temp_dir, f"page_{i}.tif")

                                            # Save the current page to the output file
                                            cv2.imwrite(output_file, tiff_file[i])
                                            #file_size = os.path.getsize( tiff_file[i].filename)
                                            print(f'{datetime.now()} Adding {output_file} to {docID}')
                                            
                                            temp_files.append(output_file)

                                    if (self.aqApi.AddPagesToDocument(docID, temp_files).status_code != 200):
                                        raise Exception(f'Error uploading files:')
                        else:
                            #if this is not a tif file, just upload it.
                            print(f'{datetime.now()} Adding {file_path} to {docID}')
                            if (self.aqApi.AddPagesToDocument(docID, [file_path]).status_code != 200):
                                raise Exception(f'Error uploading files:')             
                        #delete the file.
                        print(f"{datetime.now()} Deleting {file_path}")
                        #os.remove(file_path)
                    else:
                        print(f"{datetime.now()} error: user is not authenticated.")
                else:
                    print(f"{datetime.now()} error: document did not pass filter: {file_path}")
            else:
                print(f"{datetime.now()} error: QR Code not found: {file_path}")
        except Exception as ex:
            print(f'{datetime.now()} Error: {ex.args[0]}')
