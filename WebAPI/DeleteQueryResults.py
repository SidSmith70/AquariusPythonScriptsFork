
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


def get_input_file(default_name: str = "GridViewExport.csv") -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]

    script_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    return str(script_dir / default_name)

import utils.AquariusImaging as AquariusImaging

#************************ CONFIGURATION ***********************************************************
from dotenv import load_dotenv
load_dotenv()
username = os.environ.get("AQUARIUS_USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL")

inputFile = get_input_file()
multipage = False

#************************ CONFIGURATION ***********************************************************


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