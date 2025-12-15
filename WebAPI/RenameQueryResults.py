
########################################################################################################################
# 
# Purpose: This script reads data previously downloaded using DownloadQueryResults and renames the files as needed.
#
########################################################################################################################


from pathlib import Path
import os
#from numpy import true_divide
import pandas as pd
import shutil
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

outputFolder = os.path.dirname(inputFile)
outputFolder += '/Output'

#read csv for document indexes
indexes_df = pd.read_csv(inputFile,sep='\t', lineterminator='\n')

#read csv for pages
images_df = pd.read_csv(os.path.splitext(inputFile)[0] + 'ImageXRef.csv', sep='\t', lineterminator='\n')
for col in images_df.columns:
    print (col)
#merge the data
merged_data = pd.merge(indexes_df,images_df,left_on='doc_id',right_on='doc_id',sort=True)

#initialize docID variable
docID = ""

docCounter = 0
pageCounter = 0

#begin loop through documents
for index, row in merged_data.iterrows():

    #if this is the first page of a new document
    if (row.doc_id != docID ):

        #generate the output folder
        #iterate over columns? to use all field data?
        filePath = outputFolder + "/"  # +  str(row.Name) + "/" 

        
        print("start a new Document: " + filePath  )
        docID = row.doc_id

        #make the file path
        #os.makedirs(filePath,exist_ok=True)
        docCounter += 1

    fileName =  row["Tipo"] + '-' + str(row["NumLey"]) + '-' + str(row["Year"]) + os.path.splitext(row.FileName)[1] # docID + str(row.Page) + os.path.splitext(row.FileName)[1]
    #fileName = str(row.FileName)
    #fileName = fileName.replace("/","-")
    #fileName = fileName.replace("\\","/")
    #fileName = fileName.replace("..","")
    #fileName =  os.path.basename(fileName)

    print("copy " + str(row.FileName) + " to " + filePath + fileName)
    if (not os.path.exists(filePath)):
        os.makedirs(filePath,exist_ok=True)

    shutil.copyfile(row.FileName,filePath + fileName)
    pageCounter += 1

print("rename complete. " + str(docCounter) + " Documents, " + str(pageCounter) + " Pages exported.")
