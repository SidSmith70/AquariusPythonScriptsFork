# ******************* LOAD SETTINGS FROM .ENV FILE *******************
# THIS IS PRIMARILY USED TO STORE SENSITIVE INFORMATION.
import os
from dotenv import load_dotenv
load_dotenv()
# ********************************************************************

aquarius_api_url = os.getenv("AQUARIUSAPIURL")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

document_type_id = os.getenv("DOCTYPEID")

folder_to_watch = "./service/WatchedFolder"  # Folder to watch for new csv files
process_existing_files = True

# Mapping of document index field names to CSV column positions (0-based)
field_mappings = {
    # 'FieldName': column_index,
}

# Column index in the CSV row containing the path to the PDF file
pdf_index = 5
