#******************* LOAD SETTINGS FROM .ENV FILE ********************************************
# THIS IS PRIMARILY USED TO STORE SENSITIVE INFORMATION.
import os
from dotenv import load_dotenv
load_dotenv()
#******************* LOAD SETTINGS FROM .ENV FILE ********************************************

aquarius_api_url = os.getenv("AQUARIUSAPIURL")

username = os.getenv("USERNAME")

password = os.getenv("PASSWORD")

document_type_id = os.getenv("DOCTYPEID")

folder_to_watch = "./service/WatchedFolder"  # Folder to watch for new files

process_existing_files = True

field_mappings = {
    'TIPO': 4,  # e.g., c:\RicohScanFolder\Yabucoa\PRESTAMO AUTOS\1234.pdf -> 'PRESTAMO AUTOS' at index 3
    'cuenta_socio': 5  # e.g., c:\RicohScanFolder\Yabucoa\PRESTAMO AUTOS\1234.pdf -> '1234' at index 4
}