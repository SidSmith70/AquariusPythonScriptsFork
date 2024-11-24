#******************* LOAD SETTINGS FROM .ENV FILE ********************************************
# THIS IS PRIMARILY USED TO STORE SENSITIVE INFORMATION.
import os
from dotenv import load_dotenv
load_dotenv()
#******************* LOAD SETTINGS FROM .ENV FILE ********************************************


folders_to_watch = {
    './service/WatchedFolder':True
    # Add more folders to watch as needed separated by commas
}

aquarius_api_url = os.getenv("AQUARIUSAPIURL")

username = os.getenv("USERNAME")

password = os.getenv("PASSWORD")