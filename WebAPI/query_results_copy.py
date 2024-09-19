
########################################################################################################################
# 
# Purpose: This script uses query results the user already obtained from running a query in Aquarius Web and saving
# the results to a GridViewExport.csv file to copy the documents and images to a different Aquarius server.
#
########################################################################################################################

#************************ Imports for copier class  ***********************************************************
import utils.AquariusImaging as AquariusImaging
#************************ Imports for copier class   ***********************************************************

from datetime import datetime
import logging
import sys
#************************ CONFIGURATION ***********************************************************
# Configuration for the source server
source_server = "https://asp.aquariusimaging.com/AquariusWebAPI"
source_username = "sid@aquarius"
source_passsword = "xxxxxxx"
# Configuration for the destination server
dest_server = "https://asp.aquariusimaging.com/AquariusWebAPI"
dest_username = "sid@aquarius"
dest_password = "xxxxxxx"
#************************ CONFIGURATION ***********************************************************

#************************ LOGGING SETUP ***********************************************************
# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("FileCopyLog.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)
#************************ LOGGING SETUP ***********************************************************



#if a file was dropped on this script, use it as the input file
if (len(sys.argv) > 1):
    inputFile = sys.argv[1] 

#generate a unique id so that we can create a unique folder for this run.
uniqueID = datetime.now().strftime('%Y%m%d%H%M%S')
import time
class TimeEstimator:
    def __init__(self, total_documents):
        self.start_time = time.time()
        self.total_documents = total_documents
        self.documents_downloaded = 0

    def increment_documents_downloaded(self):
        self.documents_downloaded += 1

    def get_estimated_remaining_time(self):
        elapsed_time = time.time() - self.start_time
        average_time_per_document = elapsed_time / self.documents_downloaded if self.documents_downloaded else 0
        remaining_documents = self.total_documents - self.documents_downloaded
        estimated_remaining_time = average_time_per_document * remaining_documents
        return estimated_remaining_time
    
class DocumentCopier:
    def __init__(self, sourceApiWrapper, destinationApiWrapper, destination_doctype):
        self.sourceApiWrapper = sourceApiWrapper
        self.destinationApiWrapper = destinationApiWrapper
        self.docCounter = 0
        self.totalDocuments = 0
        self.destination_doctype = destination_doctype

    def process_documents(self, input_file):

       
        with open(input_file, 'r', encoding='UTF-8') as queryResultsData: #initialize the time estimator
            #self.time_estimator = TimeEstimator(len(queryResultsData))
            for resultLine in queryResultsData:
                docID = resultLine.split('\t')[0]
                #check that we are caught up to the last doc_id in the cross reference file.
                if docID != 'doc_id':
                                                    
                    self.process_document(docID)

        logger.info(f'Process complete! {self.docCounter} documents copied.')

    def process_document(self, docID):
                
        #self.time_estimator.increment_documents_downloaded()  
        #print(f'Copying {docID} {self.docCounter}/{self.totalDocuments} {self.docCounter/self.totalDocuments*100:.0f}% ({self.time_estimator.get_estimated_remaining_time()/60:.0f} minutes remaining)')
        docresponse = self.sourceApiWrapper.GetDocument(docID)
        if docresponse.status_code == 200:
            doc = docresponse.json()
            doc["doctype"] = self.destination_doctype
            newdocresponse = self.destinationApiWrapper.CreateDocument(doc)
            if newdocresponse.status_code == 200:
                newdocID = newdocresponse.json()
                logger.info(f'Copying document {docID} to {newdocID}')
                self.process_pages(doc,newdocID)
                self.docCounter += 1
            else:
                raise Exception(f'Error creating document {docID}. Error code: {newdocresponse.status_code}')
        else:
            raise Exception(f'Error downloading document {docID}. Error code: {docresponse.status_code}')

    def process_pages(self, doc, dest_docid,starting_page=1):

        # initialize a page files list to store the saved files for this document.
        #self.page_files = []

        for pageCounter in range(starting_page, doc["pageCount"] + 1):
            self.process_page(doc["docID"],dest_docid, pageCounter)
        

    def process_page(self, source_docid, dest_docid, pageCounter):
        
        response = self.sourceApiWrapper.GetPage(source_docid, pageCounter, "image")
        if response.status_code == 200:
            page = response.content

            # instead of writing the file to disk, we will upload the file to the destination server.
            response = self.destinationApiWrapper.AddPageContentToDocument(dest_docid, page, f'{source_docid}_{pageCounter}')
            if response.status_code == 200:
                logger.info(f'Copied page {pageCounter} from document {source_docid} to document {dest_docid}.')
            else:
                raise Exception(f'Error uploading page {pageCounter} from document {source_docid} to document {dest_docid}. Error code: {response.status_code}')
        elif response.status_code == 401:
            raise Exception(f'Unauthorized to download pages from document {source_docid}.')


try:
        
    #create the AquariusWebAPIWrapper objects for the source and destination servers
    sourceApiWrapper = AquariusImaging.AquariusWebAPIWrapper(source_server)
    sourceApiWrapper.authenticate(source_username,source_passsword)
        
    destinationApiWrapper = AquariusImaging.AquariusWebAPIWrapper(dest_server)
    destinationApiWrapper.authenticate(dest_username,dest_password)

    doc_copier = DocumentCopier(sourceApiWrapper, destinationApiWrapper,"93EEJG1D")
    inputFile = "./Migrationtest.csv"
    doc_copier.process_documents(inputFile)


except Exception as e:
    logger.error(f"An exception occurred: {str(e)}")

