
########################################################################################################################
# 
# Purpose: This script contains a class for downloading documents from Aquarius DMS in a standard and repeatable way.
# It uses the GridViewExport.csv file, which is a standard download from Aquarius DMS Web query results. It then 
# creates a cross reference file between images and the document indexes.
#
########################################################################################################################


import utils.AquariusImaging as AquariusImaging
import os
import tifftools
from datetime import datetime
import pandas as pd
import re


class CrossRefDataWriter:
    def __init__(self,inputfile,uniqueIdentifier):
        
        #establish the output file path
        self.outputPath = os.path.dirname(inputfile)
        self.imageXRefFilePath = os.path.splitext(inputfile)[0] + 'ImageXRef.csv' # outputPath + '/ImageXref.csv'
        self._last_doc_id = ''
        self._last_page = 0

        #create unique folder
        self.outputPath += '\\' + uniqueIdentifier + '\\'

        os.mkdir(self.outputPath)
    
        #create image cross reference data file.
        self.imageXRefFile = open(self.imageXRefFilePath,'ab')
    
        # write the column headers only if the file is empty
        if os.path.getsize(self.imageXRefFilePath) == 0:
            self.imageXRefFile.write(bytes('doc_id' + '\t' + 'Page' + '\t' + 'FileName' + '\n','UTF-8'))
        else: 
            # read the file and get the doc_id from the last line
            with open(self.imageXRefFilePath, 'r') as f:
                lines = f.readlines()
                line_count = len(lines)
                if line_count > 1:
                    last_line = lines[-1]
                    self._last_doc_id = last_line.split('\t')[0]
                    self._last_page = int(last_line.split('\t')[1])
    @property
    def last_doc_id(self):        
        return self._last_doc_id

    @property
    def last_page(self):
        return self._last_page
    
    def Write(self,docID,pageCounter,fileName):
        self.imageXRefFile.write(bytes(docID + '\t' + str(pageCounter) + '\t' + fileName + '\n','UTF-8'))
        self.imageXRefFile.flush()

    def Close(self):
        self.imageXRefFile.close()


def GetMergedData(inputFile):
        
    #read csv for document indexes
    indexes_df = pd.read_csv(inputFile,sep='\t', lineterminator='\n', header=0)

    #read csv for pages
    images_df = pd.read_csv(os.path.splitext(inputFile)[0] + 'ImageXRef.csv', sep='\t', lineterminator='\n', header=0)

    #merge the data
    merged_data = pd.merge(indexes_df,images_df,left_on='doc_id',right_on='doc_id',sort=True)
        
    return merged_data

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
    
   
class QueryResultsDownloader:
    def __init__(self, server, username, password):
        self.webApi = AquariusImaging.AquariusWebAPIWrapper(server)
        if (username != ""):
            self.webApi.authenticate(username, password)
        
    def authenticate(self, username, password):
        while not self.webApi.Authenticated:
            username = input("username: ")
            password = input("password: ")
            self.webApi.authenticate(username, password)

    def download_documents(self, inputFile, multiPage, uniqueIdentifier, type='image'):
        with open(inputFile, 'r', encoding='UTF-8') as queryResultsData:
            
            XrefDataWriter = CrossRefDataWriter(inputFile, uniqueIdentifier)
              # initialize the variable that determines if we are caught up to the last doc_id
            self.caughtUp = (XrefDataWriter.last_doc_id == '')

            # Count the total number of lines in the file, subtracting the header line
            self.totalDocuments = sum(1 for line in queryResultsData) - 1

            queryResultsData.seek(0)  # Reset the file pointer to the beginning

            # Initialize the time estimator
            self.time_estimator = None

            self.docCounter = 0

            self.time_estimator = TimeEstimator(self.totalDocuments - self.docCounter)

            self.process_documents(queryResultsData, XrefDataWriter, multiPage, type)

    def process_documents(self, queryResultsData, XrefDataWriter, multiPage, type):
        for resultLine in queryResultsData:
            docID = resultLine.split('\t')[0]
            #check that we are caught up to the last doc_id in the cross reference file.
            if docID != 'doc_id':
                                                
                self.process_document(docID, XrefDataWriter, multiPage, type)

        print(f'{datetime.now()} Process complete! {self.docCounter} documents downloaded.')

    def process_document(self, docID, XrefDataWriter, multiPage, type):
        self.docCounter += 1
        starting_page = 1
        if not self.caughtUp:
            if docID == XrefDataWriter.last_doc_id:
                self.caughtUp = True
                print(f'{datetime.now()} Resuming at {docID} page {XrefDataWriter.last_page}')
                starting_page = XrefDataWriter.last_page + 1
            else:
                
                print(f'{datetime.now()} Skipping {docID}, already Downloaded ')
                
                #exit the function
                return
            
        self.time_estimator.increment_documents_downloaded()  
        print(f'{datetime.now()} Downloading {docID} {self.docCounter}/{self.totalDocuments} {self.docCounter/self.totalDocuments*100:.0f}% ({self.time_estimator.get_estimated_remaining_time()/60:.0f} minutes remaining)')
        docresponse = self.webApi.GetDocument(docID)
        if docresponse.status_code == 200:
            doc = docresponse.json()
            self.process_pages(doc, docID, XrefDataWriter, multiPage, type, starting_page)
        else:
            raise Exception(f'Error downloading document {docID}. Error code: {docresponse.status_code}')

    def process_pages(self, doc, docID, XrefDataWriter, multiPage, type, starting_page):

        # initialize a page files list to store the saved files for this document.
        self.page_files = []

        for pageCounter in range(starting_page, doc["pageCount"] + 1):
            self.process_page(docID, pageCounter, XrefDataWriter,  type)
        
        if multiPage:
            if(len(self.page_files) == 1):
                pageCounter = 1
                XrefDataWriter.Write(docID,pageCounter,self.page_files[0])   
            else:
                self.create_multi_page_tiff(docID, XrefDataWriter)
        else:
            #loop through the page files and write them to the cross reference file.
            for pageCounter, page_file in enumerate(self.page_files, start=1):
                XrefDataWriter.Write(docID, pageCounter, page_file)

    def create_multi_page_tiff(self, docID, XrefDataWriter):
        newTif = None
        for tiffFile in self.page_files:
            if newTif is None:
                newTif = tifftools.read_tiff(tiffFile)
            else:
                tiftoadd = tifftools.read_tiff(tiffFile)
                newTif['ifds'].extend(tiftoadd['ifds'])
        multiTiff = self.page_files[0].lower().replace(".tif", "-multi.tif")
        tifftools.write_tiff(newTif, multiTiff)
        XrefDataWriter.Write(docID, 1, multiTiff)
        for imagefile in self.page_files:
            os.remove(imagefile)    

    def process_page(self, docID, pageCounter, XrefDataWriter,  type):
        response = self.webApi.GetPage(docID, pageCounter, type)
        if response.status_code == 200:
            self.save_page(response, docID, pageCounter, XrefDataWriter)
            
        elif response.status_code == 401:
            raise Exception(f'Unauthorized to download document {docID}.')

    def save_page(self, response, docID, pageCounter, XrefDataWriter):
        fileName = self.get_filename(response, docID, pageCounter, XrefDataWriter)
        with open(fileName, 'wb+') as imageFile:
            imageFile.write(response.content)
            self.page_files.append(fileName)

    def get_filename(self, response, docID, pageCounter, XrefDataWriter):
        fileName = response.headers['Content-Disposition']
        fileName = os.path.join(XrefDataWriter.outputPath, docID + str(pageCounter) + re.sub('.*filename=(.+)(?: |$)', '\\1', fileName))
        return fileName.replace('"', '')
    
