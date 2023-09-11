
########################################################################################################################
# 
# Purpose: This script demonstrates how to run a simple query and download documents.
#
########################################################################################################################



import requests
from requests.models import CaseInsensitiveDict
from os.path import expanduser
from datetime import datetime
import json
import re
import os


#************************ CONFIGURATION ***********************************************************
from dotenv import load_dotenv
load_dotenv()
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL") 
docType = os.environ.get("DOCTYPEID")

fieldName = 'VIN'
filterValue = 'ja*'
outputPath = expanduser("~")
#************************ CONFIGURATION ***********************************************************

#create a dated folder to output this batch of data.
currentTime = datetime.now().strftime("%Y%m%d%H%M%S")
outputPath += '/' + currentTime + '/'
os.mkdir(outputPath)

#Authenticate
if username=="":
    username=input("username: ")
if password=="":
    password=input("password: ")
creds = {'username': username,'password': password, 'grant_type':'password'}
response = requests.post(server + '/token',creds)


if response.status_code==200:

    #create data file.
    indexDataFile = open(outputPath + "indexdata" + docType + ".txt",'w')

    #get the authentication token
    token = response.json()['access_token']
    headers =  CaseInsensitiveDict()
    headers['Authorization'] = "Bearer " + token

    #get the query definition
    response = requests.get(server + "/api/QueryDefs/" + docType,headers=headers)
    queryDef=response.json()

    #set a search value
    numPolizaField = [x for x in queryDef['queryFields'] if x['fieldName'] == fieldName]
    numPolizaField[0]['searchValue']=filterValue
    jsondata = json.dumps(queryDef)

    #run the query
    payload={'json': jsondata}
    response = requests.get(server + "/api/Documents",params=payload,headers=headers)
    queryResult = response.json()
    
    #begin document loop
    startPos = int(input("Starting Position (starts at 0):"))
    endPos = startPos + int(input("Number of Documents to download (max: " + str((len(queryResult) - startPos)) + "):")) 
    for document in range(startPos,endPos):
    
        print(str(document) + ": " + queryResult[document]['docID'])
    
        dataLine = queryResult[document]['docID'] + '|'
    #   retrieve the document indexes
        for index in range(6,len(queryResult[document]['indexData'])-1) :
            dataLine = dataLine + queryResult[document]['indexData'][index]['value'] + '|'
            
        
    #   begin page loop
        for pageCounter in range(0,queryResult[document]['pageCount']):

    #       retrieve the page
            response = requests.get(server + "/api/DocPages/" + queryResult[document]['docID'] + "/" + str(pageCounter+1),headers=headers)
            fileName = response.headers['Content-Disposition']
            fileName = outputPath + re.sub('.*filename=(.+)(?: |$)','\\1',fileName)
            imageFile = open(fileName, "wb+")

    #       write the image to disk
            imageFile.write(response.content)
            indexDataFile.write(dataLine + fileName + "\n")
            

    #   end page loop

    #end document loop
    print('Process complete!')
else:
    print("Access denied: incorrect username or password.")
