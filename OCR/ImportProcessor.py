
from PIL import Image
from datetime import datetime
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import tempfile
import sys
import os

# Now you can import your script
import utils.AquariusImaging as AquariusImaging


# This class handles importing files.
class ImportProcessor():
    
    def __init__(self, config):

        self.config = config

                # Authenticate to Aquarius Imaging
        self.aqApi =  AquariusImaging.AquariusWebAPIWrapper(config['server'])                     
        self.aqApi.authenticate(config['username'], config['password'])

        # Get the query definition for the document type, and create a JSON helper class to help us build the JSON for the API calls
        if (self.aqApi.Authenticated):
            pass
        else:
            raise Exception(f'{datetime.now()} Error authenticating to Aquarius Imaging')

    def Process(self, file_path):
        try:
            if file_path.lower().endswith('.tif') or file_path.lower().endswith('.jpg'):
                print(f"{datetime.now()} Processing {file_path}")
                
                img = Image.open(file_path)
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                
                # Read the barcode from the image
                barcodes = decode(img_cv)
                doc_id = None
                for barcode in barcodes:
                    barcode_data = barcode.data.decode('utf-8')
                    barcode_type = barcode.type
                    print(f"Found {barcode_type} barcode: {barcode_data}")
                    if len(barcode_data) == 8:
                        doc_id = barcode_data
                        
                        break
                
                doc_id = 'W2SQXH6W'
                if doc_id:
                    if (file_path.lower().endswith('.tif')):                    
                        temp_files = []
                        # Create a temporary directory to store the single-page TIFF files.
                        # When we exit this scope, the files are automatically deleted.
                        with tempfile.TemporaryDirectory() as temp_dir:
                        
                            # Open the multipage TIFF file
                            tiff_file = []

                            #tiff_file = cv2.imread(file_path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_ANYCOLOR)
                            retbool, tiff_file = cv2.imreadmulti(mats=tiff_file,
                                                        filename=file_path,
                                                        flags=cv2.IMREAD_ANYCOLOR)
                            
                            # Iterate over each page in the TIFF file
                            if len(tiff_file) > 0:
                                for i in range(len(tiff_file)):
                                                                                                                    
                                    # Create a filename for the single-page TIFF file
                                    output_file = os.path.join(temp_dir, f"page_{i}.tif")

                                    # Save the current page to the output file
                                    cv2.imwrite(output_file, tiff_file[i])
                                    #file_size = os.path.getsize( tiff_file[i].filename)
                                    print(f'{datetime.now()} Adding {output_file} to {doc_id}')
                                    
                                    temp_files.append(output_file)

                                if (self.aqApi.AddPagesToDocument(doc_id, temp_files).status_code != 200):
                                    raise Exception(f'Error uploading files:')
                    else:
                        #if this is not a tif file, just upload it.
                        print(f'{datetime.now()} Adding {file_path} to {doc_id}')
                        if (self.aqApi.AddPagesToDocument(doc_id, [file_path]).status_code != 200):
                            raise Exception(f'Error uploading files:')             
                    
                    #delete the file.
                    print(f"{datetime.now()} Deleting {file_path}")
                    #os.remove(file_path)
            
        except Exception as ex:
            print(f'{datetime.now()} Error: {ex.args[0]}')

