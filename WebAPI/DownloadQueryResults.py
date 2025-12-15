
########################################################################################################################
# 
# Purpose: This script downloads the query results the user already obtained from running a query in Aquarius Web and saving
# the results to a GridViewExport.csv file. It then downloads the images associated with the query results.
#
########################################################################################################################

from pathlib import Path
from datetime import datetime
import sys

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

import utils.AquariusDownloader as AquariusDownloader

#************************ CONFIGURATION ***********************************************************
from dotenv import load_dotenv
import os
load_dotenv()
username = os.environ.get("AQUARIUS_USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL")

inputFile = get_input_file()
multipage = False
type = 'image'
#************************ CONFIGURATION ***********************************************************

#generate a unique id so that we can create a unique folder for this run.
uniqueID = datetime.now().strftime('%Y%m%d%H%M%S')

try:
    #download the images
    aqdownloader = AquariusDownloader.QueryResultsDownloader(server,username,password)

    aqdownloader.download_documents(inputFile,multipage,uniqueID,type)

except Exception as e:
    print (f"An exception occurred: {str(e)}")

