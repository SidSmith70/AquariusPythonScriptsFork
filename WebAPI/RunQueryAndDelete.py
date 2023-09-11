
########################################################################################################################
# 
# Purpose: This script will run a query using the Aquarius Web API and delete the resulting documents.
#
########################################################################################################################

from datetime import datetime
import utils.AquariusImaging as AquariusImaging
import json


#************************ CONFIGURATION ***********************************************************
from dotenv import load_dotenv
import os
load_dotenv()
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
server = os.environ.get("AQUARIUSAPIURL") 
doctypeCode = os.environ.get("DOCTYPEID")

queryField = 'Status'
queryValue = 'Funded'
#************************ CONFIGURATION ***********************************************************


def DeleteResults(queryResults):
    for document in queryResults:

        docID = document['docID']
        if (docID != 'doc_id'):
            
            response = aqApi.DeleteDocument(docID)

            print('Delete ' + docID + " " + str(response.status_code))
        


#generate a unique id so that we can create a unique folder for this run.
uniqueID = datetime.now().strftime('%Y%m%d%H%M%S')


# STEP 1: get query def
aqApi =  AquariusImaging.AquariusWebAPIWrapper(server)
aqApi.authenticate(username,password)
response = aqApi.GetQueryDefinition(doctypeCode)

if (response.status_code==200):
    queryDef = response.json()

# STEP 2: set search value
queryField = list(filter(lambda x: (x['fieldName'] == queryField), queryDef['queryFields']))[0]
queryField['searchValue'] = queryValue

# STEP 3: run the query
response = aqApi.RunQuery(json.dumps(queryDef))
if (response.status_code==200):
    queryResults = response.json()
# >>> from datetime import datetime, timedelta
# >>> past = datetime.now() - timedelta(days=1)
# >>> present = datetime.now()
# >>> past < present
# True
# >>> datetime(3000, 1, 1) < present
# False
# >>> present - datetime(2000, 4, 4)
# datetime.timedelta(4242, 75703, 762105)


# STEP 4: delete the queryResults
DeleteResults(queryResults)

print('Process complete!')

