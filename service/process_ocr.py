##################################################################################################
# This class runs the ocr process on the image files.
# It uses the pytesseract library to extract text from the image files.
# The extracted text is saved to a text file with the same name as the image file.
##################################################################################################

import pytesseract
from PIL import Image
from datetime import datetime

# This class handles importing files.
class OCRProcessor():
    
    def __init__(self, config):

        self.config = config
   
    def Process(self, file_path):

       #run the tessaract OCR process
        try:
            if file_path.lower().endswith('.tif') or file_path.lower().endswith('.jpg'):
                print(f"{datetime.now()} Processing  {file_path}")
                
                img = Image.open(file_path)

                #run the ocr
                config='-c preserve_interword_spaces=1 --oem {} --psm {} -l {}'.format('3','1','eng+spa')
                ocr_text = pytesseract.image_to_string(img, config=config).strip()


                #save the text file
                textkey = file_path[0:-4] + '.txt'
                with open(textkey, 'w') as f:
                    f.write(ocr_text)
                    print(f"{datetime.now()} Saved text file {textkey}")

        except Exception as ex:
            print(f'{datetime.now()} Error: {ex.args[0]}')
