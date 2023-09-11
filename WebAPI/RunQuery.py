
########################################################################################################################
# 
# Purpose: This script demonstrates how to run a query in Aquarius DMS using the Aquarius Web API.
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
doctypeID = os.environ.get("DOCTYPEID")
#************************ CONFIGURATION ***********************************************************


#generate a unique id so that we can create a unique folder for this run.
#uniqueID = datetime.now().strftime('%Y%m%d%H%M%S')


# STEP 1: get query def
aqApi =  AquariusImaging.AquariusWebAPIWrapper(server)
aqApi.authenticate(username,password)
response  = aqApi.GetQueryDefinition(doctypeID)

if (response.status_code==200):
    queryDef = response.json()
        

# STEP 2: set search value
queryDef['queryFields'][0]['searchValue']='test'
#queryDef['queryFields'][5]['operatorString']='ne'

# STEP 3: run the query
response = aqApi.RunQuery(json.dumps(queryDef).replace('"',"'"))
if (response.status_code==200):
    results = response.json()

    # STEP 4: save the results
    print(results)

else:
    print(response.status_code)
    print(response.text)
    print(response.reason)

 
