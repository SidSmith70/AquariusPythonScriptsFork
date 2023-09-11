
########################################################################################################################
# 
# Purpose: This script downloads the query results obtained from running a query in Aquarius Web and saving
# the results to a GridViewExport.csv file. It then downloads the images associated with the query results.
# Finally, this script renames the files based on the data in the query results.
#
########################################################################################################################



import utils.AquariusDownloader as AquariusDownloader
import sys
import os
import pandas as pd
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
AquariusDownloader.DownloadImagesFromQueryResults(inputFile,username,password,server,multipage,uniqueID,type)


outputFolder = os.path.dirname(inputFile)
outputFolder += '/Output'

#read csv for document indexes
indexes_df = pd.read_csv(inputFile,sep='\t', lineterminator='\n')

#read csv for pages
images_df = pd.read_csv(os.path.splitext(inputFile)[0] + 'ImageXRef.csv', sep='\t', lineterminator='\n')

#merge the data
merged_data = pd.merge(indexes_df,images_df,left_on='doc_id',right_on='doc_id',sort=True)

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

    fileName = '{:04}'.format(row["Book"]) + '-' + '{:04}'.format(row["Page_x"]) + os.path.splitext(row["FileName"])[1]
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
