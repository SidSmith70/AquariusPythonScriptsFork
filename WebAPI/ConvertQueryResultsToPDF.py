
########################################################################################################################
# 
# Purpose: This script uses the output from DownloadQueryResults, and converts the images to pdf while renaming them as needed.
#
########################################################################################################################

import os
import pandas as pd
import img2pdf

#initialize variable(s)
inputFile = "./GridViewExport.csv"

def GenerateFileName(row):
    
    #Configure the file naming convention here!!
    fileName = row.Type + "-" + str(row.Year) + "-" + row['Name'] + "-" + row.doc_id + ".pdf"

    #remove illegal characters from filename:
    fileName = fileName.replace("/","-")
    fileName = fileName.replace(":","-")

    return fileName


class PDFWriter:
    def __init__(self,ID,pdfFilePath) -> None:
        self.filepath = pdfFilePath
        self.pageList=[]
        self.ID = ID
        print(ID)
        
    def WritePDF(self):
        if (len(self.pageList) > 0):
            print('Creating pdf: ' + self.filepath)
            os.makedirs(os.path.dirname(self.filepath),exist_ok=True)
            with open(self.filepath,"wb") as f:
                f.write(img2pdf.convert(self.pageList))

    def AddPage(self,filepath):
        self.pageList.append(filepath)

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


