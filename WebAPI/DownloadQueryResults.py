
########################################################################################################################
# 
# Purpose: This script downloads the query results obtained from running a query in Aquarius Web and saving
# the results to a GridViewExport.csv file. It then downloads the images associated with the query results.
#
########################################################################################################################

import utils.AquariusDownloader as AquariusDownloader
from datetime import datetime
import sys

#************************ CONFIGURATION ***********************************************************
from dotenv import load_dotenv
import os
load_dotenv()
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL") 

inputFile = "./GridViewExport.csv"
multipage = False
type = 'image'
#************************ CONFIGURATION ***********************************************************


#if a file was dropped on this script, use it as the input file
if (len(sys.argv) > 1):
    inputFile = sys.argv[1] 

#generate a unique id so that we can create a unique folder for this run.
uniqueID = datetime.now().strftime('%Y%m%d%H%M%S')

#download the images
try:
    AquariusDownloader.DownloadImagesFromQueryResults(inputFile,username,password,server,multipage,uniqueID,type)
except Exception as e:
    print(f"An exception occurred: {str(e)}")
