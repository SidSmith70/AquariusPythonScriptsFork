
########################################################################################################################
# 
# Purpose: This script contains classes for interacting with the Aquarius WEB API.
#
########################################################################################################################

import requests
from requests.models import CaseInsensitiveDict
import os
import time
from datetime import datetime
from datetime import timedelta
import json

class AquariusWebAPIWrapper:
    
    def __init__(self,server):
        self.server=server
        self.Authenticated =False
    
    #Authenticate
    def authenticate(self,username,password):
        
        creds = {'username': username,'password': password, 'grant_type':'password'}
        response = requests.post(self.server + '/token',creds)
        headers=""

        self.__readToken(response)
        
    def __refreshToken(self):
       
        if (datetime.now() >= self.expiresAt):
            #refresh the token
            print(f'{datetime.now()} refreshing access token')

            creds = {'refresh_token': self.refresh_token, 'grant_type':'refresh_token'}
            response = requests.post(self.server + '/token',creds)
            
            self.__readToken(response)

    def __readToken(self,response):
        #if authentication was successful
        if response.status_code==200:
            #get the authentication token
            token = response.json()['access_token']
            self.expiresAt = datetime.now() + timedelta(seconds=response.json()['expires_in'] - 120)
            print(f'{datetime.now()} token expires at: {str(self.expiresAt)}')
            self.refresh_token = response.json()['refresh_token']
            self.headers =  CaseInsensitiveDict()
            self.headers['Authorization'] = 'Bearer ' + token

            self.Authenticated = True
        else:
            print(f'{datetime.now()} Error reading token: {str(response.status_code)} {response.text}')
    
    #retrieve a page
    def GetPage(self,docID,pageCounter,type):
        

        while True:
            self.__refreshToken()
            try:
                if (type=='image'):
                    response = requests.get(self.server + '/api/DocPages/' + docID + '/' + str(pageCounter),headers=self.headers)
                
                else:
                    response = requests.get(self.server + '/api/DocPages/' + docID + '/' + str(pageCounter) + '/' + type,headers=self.headers)
                
                break
            except:
                print(f"{datetime.now()} retry {docID} Page: { str(pageCounter)}" )
                time.sleep(3)
        
        return response


    #retrieve a document
    def GetDocument(self,docID):

        while True:
            self.__refreshToken()

            try:
                response = requests.get(self.server + '/api/Documents/' + docID,headers=self.headers)
                break
            except: 
                print(f"{datetime.now()} retry {docID}")
                time.sleep(3)

        return response
    
    def AddPageToDocument(self,docID, filepath):
        self.__refreshToken()
        payload={}
        files=[
        ('file',(os.path.basename(filepath),open(filepath,'rb'),'image/tiff'))
        ]
        response = requests.request("POST", self.server + '/api/DocPages/' + docID, headers=self.headers, data=payload, files=files)
        
        #print(response.text) will always be 1 because it's one page at a time.

        return response


    def AddPagesToDocument(self, docID, filepaths):
        self.__refreshToken()

        MB = 1024 * 1024  # Bytes in a Megabyte
        MAX_SIZE = 4 * MB

        def send_files(files_to_send):
            """Helper function to send files."""
            response = requests.request(
                "POST", self.server + '/api/DocPages/' + docID, headers=self.headers, files=files_to_send
            )
            return response

        accumulated_size = 0
        accumulated_files = []
        last_response = None  # This will hold the last response

        for filepath in filepaths:
            file_size = os.path.getsize(filepath)
            
            # If the current file alone exceeds 4MB
            if file_size > MAX_SIZE:
                # Send accumulated files first (if any)
                if accumulated_files:
                    print(f"{datetime.now()} sending {len(accumulated_files)} files")
                    last_response = send_files(accumulated_files)
                    accumulated_files = []
                    accumulated_size = 0

                # Send the large file
                last_response = send_files([('file', (os.path.basename(filepath), open(filepath, 'rb'), 'image/tiff'))])
                continue

            # If adding the current file exceeds the 4MB limit
            if accumulated_size + file_size > MAX_SIZE:
                print(f"{datetime.now()} sending {len(accumulated_files)} files")
                last_response = send_files(accumulated_files)
                accumulated_files = []
                accumulated_size = 0

            # Add the current file to the accumulator
            accumulated_files.append(('file', (os.path.basename(filepath), open(filepath, 'rb'), 'image/tiff')))
            accumulated_size += file_size

        # Send any remaining files
        if accumulated_files:
            print(f"{datetime.now()} sending {len(accumulated_files)} files")
            last_response = send_files(accumulated_files)

        return last_response


    
    def CreateDocument(self,newDocumentJson):
        self.__refreshToken()
        
        response = requests.post(self.server + '/api/Documents/', json=newDocumentJson, headers=self.headers)

        return response

    def DeleteDocument(self,docID):
        self.__refreshToken()
        try:
            response = requests.delete(self.server + '/api/Documents/' + docID,headers=self.headers)
            return response
        except:
            print(f"{datetime.now()} error deleting document: {response}" )
        
    def GetQueryDefinition(self,doctypeID):

        self.__refreshToken()

        try:
            response = requests.get(self.server + '/api/QueryDefs/' + doctypeID,headers=self.headers)
            
        except: 
            print(f"{datetime.now()} retry {doctypeID}" )
            time.sleep(3)
        #check for good response.
        # 
        return response
     

    def RunQuery(self,query):
        
        while True:

            self.__refreshToken()

            try:
                response = requests.get(self.server + '/api/Documents?json=' + query,headers=self.headers)
                break
            except: 
                print(f"{datetime.now()} retry query")
                time.sleep(3)

        return response 
    
class AQJsonHelper:
 
    def __init__(self, doctypeCode,fieldMap, queryDef):
        self.doctypeCode = doctypeCode
        self.fieldMap = fieldMap
        self.queryDef = queryDef     

    def new_document_JSON(self,indexValues):
            #create json for new document
            
        indexData = []
        for field, value in self.fieldMap.items():
            indexData.append({"fieldName": field, "value": indexValues[value]})
            
        newDocumentJson = {
            "application": None,
            "doctype": self.doctypeCode,
            "pages": [],
            "docID": None,
            "indexData": indexData
        }
        return newDocumentJson

    def query_JSON(self,indexValues):
        #create json for query

        queryFields=[]
        ft = self._queryfieldDictionary()
        for field, value in self.fieldMap.items():
           
            fieldName = ft.get(field)
            if (field != ""):
                queryFields.append({'searchValue': indexValues[value], 'operatorString': 'eq', 'fieldName': fieldName, 'description': field, 'maxLength': 0, 'listValues': []})

        thisQuery = self.queryDef
        thisQuery["queryFields"] = queryFields
        return json.dumps(thisQuery)
  
    def _queryfieldDictionary(self):
            #use the query definition to create a dictionary of field names and field descriptions.
            #this is important because queries use field names, not the description.
            tb = {}
            
            for item in self.queryDef['queryFields']:
                tb[item['description']] = item['fieldName']
            return tb



