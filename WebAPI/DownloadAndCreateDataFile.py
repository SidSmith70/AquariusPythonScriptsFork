
########################################################################################################################
# 
# Purpose: This script downloads the query results the user already obtained from running a query in Aquarius Web and saving
# the results to a GridViewExport.csv file. It then exports the data from the query results to a text file, including the configured data fields.
#
########################################################################################################################

import os
import utils.AquariusImaging as AquariusImaging
import utils.AquariusDownloader as AquariusDownloader
from datetime import datetime
import sys
#*********************************    initialize variables    ***************************************************************
from dotenv import load_dotenv
load_dotenv()
musername = os.environ.get("USERNAME")
mpassword = os.environ.get("PASSWORD")
mserver = os.environ.get("AQUARIUSAPIURL")  

fields = ["Grantor","Grantee","Book","Page_x","Date "]
inputFile = "GridViewExport.csv"

#************************ CONFIGURATION ***********************************************************


#if a file was dropped on this script, use it as the input file
if (len(sys.argv) > 1):
    inputFile = sys.argv[1] 


#Download the images as multipage tiffs
#create a unique identifier
uniqueID = datetime.now().strftime('%Y%m%d%H%M%S')

aqdownloader = AquariusDownloader.QueryResultsDownloader(mserver,musername,mpassword)
try:
    aqdownloader.download_documents(inputFile,True,uniqueID,'image')

    #get the merged data between query results and downloaded images
    merged_data = AquariusDownloader.GetMergedData(inputFile)

    #initialize variables
    docID = ""
    docCounter = 0


    #begin loop through documents
    with open(os.path.dirname(inputFile) + '\\'+ uniqueID + '\\instruments' + uniqueID + '.txt', 'w') as f:
        for index, row in merged_data.iterrows():

            #if this is not the first line of the file with the column names
            if (row.doc_id != docID ):
                dataLine =""
                for field in fields:
                    dataLine += str(row[field]) + ","
                
                dataLine  += row.FileName

                f.write(dataLine)
                f.write('\n')
            
                docCounter += 1

                docID = row.doc_id

    print("Datafile creation complete. " + str(docCounter) + " Documents added.")
    input("Press Enter to continue...")

except Exception as e:
    print (f"An exception occurred: {str(e)}")

