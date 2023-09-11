
########################################################################################################################
# 
# Purpose: This script demonstrates how to create a document in Aquarius DMS using the Aquarius Web API.
#
########################################################################################################################


import utils.AquariusImaging as AquariusImaging

#************************ CONFIGURATION ***********************************************************
from dotenv import load_dotenv
import os
load_dotenv()
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL")  
doctypeID = os.environ.get("DOCTYPEID")
#************************ CONFIGURATION ***********************************************************


webApi=AquariusImaging.AquariusWebAPIWrapper(server)

if (username != ""):
    webApi.authenticate(username,password)

while webApi.Authenticated  == False:
            username=input("username: ")
            password=input("password: ")
            webApi.authenticate(username,password)

#create json for new document
newDocumentJson = {
    "application": None,
    "doctype": doctypeID,
    "pages": [],
    "docID": None,
    "indexData": [
        {
            "fieldName": "Employee Name",
            "value": "Nelson"
        }
    ]
}

#create the document and get the docid
response = webApi.CreateDocument(newDocumentJson)
if (response.status_code) == 200:
    docid = response.json()

print(docid)

#add images to the docid
print(webApi.AddPageToDocument(docid,"cropme.tif").status_code)