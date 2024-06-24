
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
            "Account Number": 2,
            "Customer Name":3,
            "Country": 0,
            "Branch":1,
            "Date":4,
            "Status": 5
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
def extract_file_name_data(file_path):
    
    try:

        #get the filename without the extension and without the full path.
        filename = os.path.splitext(os.path.basename(file_path))[0]

        # split the values out of the filename delimited by a underscore.
        return filename.split("_")
        
    except:
        print(f'{datetime.now()} Error extracting data from filename {file_path}')
        return None

# Create a MyHandler instance to handle the event
handler =  AquariusFileHandler(doctypeCode,QRFieldMap,server,username,password,appendExistingDocuments,filter,extract_file_name_data)

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
