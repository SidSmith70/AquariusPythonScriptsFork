
########################################################################################################################
# 
# Purpose: This script imports data into Aquarius DMS with support for various methods for indexing the document.
#
########################################################################################################################

import time
import cv2
import os
from urllib.parse import unquote
from datetime import datetime
from utils.AquariusFileHandler import AquariusFileHandler
from watchdog.observers import Observer
from dotenv import load_dotenv

import pyodbc

#******************* CONFIGURATION  ********************************************
load_dotenv()
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
doctypeCode = os.environ.get("DOCTYPEID")
server = os.environ.get("AQUARIUSAPIURL")   

folderToWatch = '/media/sid/New Volume/CFGTest2'  # 'c:\\temp\\cfgtest\\'

QRFieldMap = {
    "Account Number": {"index": 2, "type": "text"},
    "Customer Name": {"index": 3, "type": "text"},
    "Country": {"index": 0, "type": "text"},
    "Branch": {"index": 1, "type": "text"},
    "Date": {"index": 4, "type": "date"},
    "Status": {"index": 5, "type": "text"}
}

appendExistingDocuments = False
filter = ""  #"Status = ACTIVE"

#************************ CONFIGURATION ***********************************************************


if os.path.exists(folderToWatch) == False:
    raise Exception(f'{datetime.now()} Error: {folderToWatch} does not exist')

# Extract data from the QR code in the first image in the multipage tiff file
def extract_qr_code_data(file_path):
    from pyzbar.pyzbar import decode
    try:
 
        img =  cv2.imread(file_path)
        decoded_objects = decode(img)
        if decoded_objects:            
 
            # Return the first QR code value as a string
            qr_code_value = decoded_objects[0].data.decode('utf-8')
            if qr_code_value:
 
                print(f'{datetime.now()} QR Code Value: {qr_code_value}')
                return qr_code_value.split("|")
            else:
                return None
        else:
            return None
    except:
        print(f'{datetime.now()} Error reading QR code')
        return None

# Extract data elements from the filename
def extract_metadata_from_file_name(file_path):
    
    try:

        file_path=unquote(file_path)
 
        #get the filename without the extension and without the full path.
        filename = os.path.splitext(os.path.basename(file_path))[0]
 
        # split the values out of the filename delimited by a underscore.
        values = filename.split("_")
 
        # lookup the interesting data from the sql database using the first value in the filename.
        keydata = values[0]
        if (len(keydata) != 9):
            interesting_data = lookup_sql_data(keydata)
            if interesting_data:
                values[0] = interesting_data
            else:
                raise ValueError(f"Unable to retrieve data for: {keydata} from the database.")
        return format_values_based_on_type(values)
        
    except:
        print(f'{datetime.now()} Error extracting data from filename {file_path}')
        return None


def lookup_sql_data(keydata):

    # Define the connection string.
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:localhost\sqlexpress;DATABASE=AccountsPayable;UID=xxxxx;PWD=xxxxx'

    # Use the with statement to ensure the connection is closed automatically.
    with pyodbc.connect(connection_string) as conn:
        # Create a cursor from the connection within the with block.
        with conn.cursor() as cursor:
           
            # Execute the query.
            cursor.execute("select vendor_number from checks where doc_id = ?", keydata)
            
            # Fetch the first row.
            row = cursor.fetchone()

            # Return the interesting data.
            if row:
                
                return row[0]
            
            else:
                return None
            


def format_values_based_on_type(indexValues):
    for i, val in enumerate(indexValues):
        # Find the corresponding field in QRFieldMap using the index
        for field, settings in QRFieldMap.items():
            if settings["index"] == i:
                field_type = settings["type"]
                
                # Update the value based on the type
                if field_type == "date":
                    if len(val) == 8 and val.isdigit():
                        try:
                            dt = datetime.strptime(val, '%Y%m%d')
                            indexValues[i] = dt.strftime('%m/%d/%Y')
                        except ValueError:
                            print(f'{datetime.now()} Not a valid date: {val}')
                elif field_type == "text":
                    # Example transformation for text, if needed
                    indexValues[i] = val.strip()
                # Add other type cases as necessary
    return indexValues

def ProcessAll(folderToWatch):

    #to process all files in the folder:
    for root, _, files in os.walk(folderToWatch):
            for filename in files:
                # print the size of the file
                #if filename.lower().endswith('.tif'):
                    file_path = os.path.join(root, filename)
                    
                    handler.ProcessFile(file_path)
    #            try:
    #                print(extract_metadata_from_file_name(filename))
    #            except:
    #                print('Error on File')

# Create a MyHandler instance to handle the event
handler =  AquariusFileHandler(doctypeCode,QRFieldMap,server,username,password,appendExistingDocuments,filter,extract_metadata_from_file_name)

# Create an observer to watch the folder for file system events
observer = Observer()
observer.schedule(handler, folderToWatch, recursive=True)
observer.start()

try:
    # Initialize a time counter
    timecounter = 0

    while True:
        # Process all files in the folder every x minutes
        if timecounter == 0:
            ProcessAll(folderToWatch)

        # increment a counter every 5 seconds
        timecounter += 5
        time.sleep(5)

        # Process all files in the folder every x minutes
        if timecounter >= 3000000:
            ProcessAll(folderToWatch)
            timecounter = 0

except KeyboardInterrupt:
    observer.stop()
observer.join()

