
########################################################################################################################
# 
# Purpose: This script uses the output from DownloadQueryResults, and converts the images to pdf while renaming them as needed.
#
########################################################################################################################

from pathlib import Path
import os
import pandas as pd
import img2pdf
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

#initialize variable(s)
inputFile = get_input_file()

def GenerateFileName(row):
    
    #Configure the file naming convention here!!
    fileName = row.Division   # + ".pdf" # row.Type + "-" + str(row.Year) + "-" + row['Name'] + "-" + row.doc_id + ".pdf"

    #remove illegal characters from filename:
    fileName = fileName.replace("/","-")
    fileName = fileName.replace(":","-")
    fileName = fileName.replace(".","")

    fileName += ".pdf"

    return fileName


class PDFWriter:
    def __init__(self,ID,pdfFilePath) -> None:
        self.filepath = pdfFilePath
        self.pageList=[]
        self.ID = ID
        print(ID)

    def WritePDF(self):
        if (len(self.pageList) > 0):
            output_path = self._get_unique_filepath()
            print('Creating pdf: ' + output_path)
            os.makedirs(os.path.dirname(output_path),exist_ok=True)
            with open(output_path,"wb") as f:
                f.write(img2pdf.convert(self.pageList))

    def AddPage(self,filepath):
        self.pageList.append(filepath)

    def _get_unique_filepath(self):
        base, extension = os.path.splitext(self.filepath)
        candidate = self.filepath
        counter = 1

        while os.path.exists(candidate):
            candidate = f"{base}({counter}){extension}"
            counter += 1

        return candidate

#start main function
outputFolder = os.path.dirname(inputFile) + '/Output'

#read csv for document indexes
indexes_df = pd.read_csv(inputFile,sep='\t', lineterminator='\n')

#read csv for pages
images_df = pd.read_csv(os.path.splitext(inputFile)[0] + 'ImageXRef.csv', sep='\t', lineterminator='\n')
    
#merge the data
merged_data = pd.merge(indexes_df,images_df,left_on='doc_id',right_on='doc_id',sort=True)

#initialize variables
docCounter = 0
pageCounter = 0

PDF=PDFWriter("","")

#begin loop through documents
for index, row in merged_data.iterrows():
    try:
        #if this is the first page of a new document
        if (row.doc_id != PDF.ID ):

            #save the previous pages to pdf
            PDF.WritePDF()
                
            #generate the next output file
            filename = GenerateFileName(row)
            filePath = outputFolder + "/" +  filename[0:len(filename)-4] + "/" + filename
            
            #instantiate the pdf writer
            PDF = PDFWriter(row.doc_id,filePath)
        
            #increment the document counter
            docCounter += 1

        #add image to the list of pages for this document
        PDF.AddPage(row.FileName)
        pageCounter += 1
    except:
        print("Error in " + row.doc_id + ". Skipping.")

#be sure the write the last document
PDF.WritePDF()

print("rename complete. " + str(docCounter) + " Documents, " + str(pageCounter) + " Pages exported.")


