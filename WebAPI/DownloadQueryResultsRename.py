
########################################################################################################################
# 
# Purpose: This script downloads the query results the user already obtained from running a query in Aquarius Web and saving
# the results to a GridViewExport.csv file. It downloads the images associated with the query results, then
# renames the files based on the data in the query results.
#
########################################################################################################################


import utils.AquariusDownloader as AquariusDownloader
import sys
import os
import shutil
from datetime import datetime

#************************ CONFIGURATION ***********************************************************
from dotenv import load_dotenv
load_dotenv()
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL") 

inputFile = "./GridViewExport.csv"
multipage = True
type = 'image'
#************************ CONFIGURATION ***********************************************************


#if a file was dropped on this script, use it as the input file
if (len(sys.argv) > 1):
    inputFile = sys.argv[1] 

#generate a unique id so that we can create a unique folder for this run.
uniqueID = datetime.now().strftime('%Y%m%d%H%M%S')

#download the images
aqdownloader = AquariusDownloader.QueryResultsDownloader(server,username,password)
try:
    aqdownloader.download_documents(inputFile,multipage,uniqueID,type)
    outputFolder = os.path.dirname(inputFile)
    outputFolder += '/Output'
   
    #get the merged data between query results and downloaded images
    merged_data = AquariusDownloader.GetMergedData(inputFile)
    
    #print out the column headers for user reference.
    print("Column Headers: ")
    for col in merged_data.columns:
        print (col)

    #initialize docID variable
    docID = ""

    docCounter = 0
    pageCounter = 0

    #begin loop through documents
    for index, row in merged_data.iterrows():

        #if this is the first page of a new document
        if (row.doc_id != docID ):

            #generate the output folder
            #iterate over columns? to use all field data?
            filePath = outputFolder + "/"  # +  str(row.Name) + "/" 

            
            print("start a new Document: " + filePath  )
            docID = row.doc_id

            #make the file path
            #os.makedirs(filePath,exist_ok=True)
            docCounter += 1

        fileName = '{:04}'.format(row["Employee Number"]) + '-' + os.path.splitext(row["FileName"])[1]
        #fileName = str(row.FileName)
        #fileName = fileName.replace("/","-")
        #fileName = fileName.replace("\\","/")
        #fileName = fileName.replace("..","")
        #fileName =  os.path.basename(fileName)

        print("copy " + str(row.FileName) + " to " + filePath + fileName)
        if (not os.path.exists(filePath)):
            os.makedirs(filePath,exist_ok=True)

        shutil.move(row.FileName,filePath + fileName)
        pageCounter += 1

    print("rename complete. " + str(docCounter) + " Documents, " + str(pageCounter) + " Pages exported.")

except Exception as e:
    print (f"An exception occurred: {str(e)}")
