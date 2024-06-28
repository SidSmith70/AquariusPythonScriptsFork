
########################################################################################################################
# 
# Purpose: This script imports data into Aquarius DMS with support for various methods for indexing the document.
#
########################################################################################################################

import time
import cv2
import os
from datetime import datetime
from utils.AquariusFileHandler import AquariusFileHandler
from watchdog.observers import Observer
from dotenv import load_dotenv

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

        #get the filename without the extension and without the full path.
        filename = os.path.splitext(os.path.basename(file_path))[0]

        # split the values out of the filename delimited by a underscore.
        values = filename.split("_")
        return format_values_based_on_type(values)
        
    except:
        print(f'{datetime.now()} Error extracting data from filename {file_path}')
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
                            dt = datetime.strptime(val, '%m%d%Y')
                            indexValues[i] = dt.strftime('%m/%d/%Y')
                        except ValueError:
                            print(f'{datetime.now()} Not a valid date: {val}')
                elif field_type == "text":
                    # Example transformation for text, if needed
                    indexValues[i] = val.strip()
                # Add other type cases as necessary
    return indexValues


# Create a MyHandler instance to handle the event
handler =  AquariusFileHandler(doctypeCode,QRFieldMap,server,username,password,appendExistingDocuments,filter,extract_metadata_from_file_name)

#to process all files in the folder:
for root, _, files in os.walk(folderToWatch):
        for filename in files:
            # print the size of the file
            if filename.lower().endswith('.tif'):
                file_path = os.path.join(root, filename)
                
                handler.ProcessFile(file_path)


# Create an observer to watch the folder for file system events
observer = Observer()
observer.schedule(handler, folderToWatch, recursive=True)
observer.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()
observer.join()
