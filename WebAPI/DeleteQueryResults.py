
########################################################################################################################
# 
# Purpose: This script uses the results of a Aquarius Web Query to delete the documents from the DMS.
#
########################################################################################################################

from pathlib import Path
import sys
import os

def add_repo_root_to_path():
    script_path = Path(__file__).resolve() if "__file__" in globals() else Path.cwd()
    root_dir = script_path.parent.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))

add_repo_root_to_path()

import utils.AquariusImaging as AquariusImaging

#************************ CONFIGURATION ***********************************************************
from dotenv import load_dotenv
load_dotenv()
username = os.environ.get("AQUARIUS_USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL")  

inputFile = "./GridViewExport.csv"
multipage = False

#************************ CONFIGURATION ***********************************************************


#if a file was dropped on this script, use it as the input file
if (len(sys.argv) > 1):
    inputFile = sys.argv[1] 

#delete the documents
webApi=AquariusImaging.AquariusWebAPIWrapper(server)

if (username != ""):
    webApi.authenticate(username,password)

while webApi.Authenticated  == False:
            username=input("username: ")
            password=input("password: ")
            webApi.authenticate(username,password)


#read the text file
queryResultsData = open(inputFile, 'r')

#begin document loop
for resultLine in queryResultsData:

    docID = resultLine.split('\t')[0]

    if (docID != 'doc_id'):
        
        response = webApi.DeleteDocument(docID)

        print(docID + " " + str(response.status_code))
        
print('Process complete!')