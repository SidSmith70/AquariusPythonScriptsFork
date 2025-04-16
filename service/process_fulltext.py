
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os
import pysolr

# This class handles the file system events for the folder being watched
class TextFileHandler(FileSystemEventHandler,):

    def __init__(self, config):
        
        self.config  =config

    
    def Process(self,file_path):
        try:
            if file_path.lower().endswith('.txt'):
                self.ProcessText(file_path)
            elif file_path.lower().endswith('.did'):
                self.ProcessDID(file_path)
        except Exception as ex:
            print(f'{datetime.now()} Error: {ex.args[0]}')
        
    def ProcessText(self, file_path):

       #extract the text and send to solr
        try:
            print(f"{datetime.now()} Processing TEXT  {file_path}")
            
            #for text files, read all the text into a string
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                full_text = f.read()

                #send the text to solr
                solr = pysolr.Solr(self.config['solrUrl']  , always_commit=True, timeout=10)
                
                solrId = file_path
                
                # replace the path with the network path
                for pair in self.config['path_replacement_pairs']:
                    solrId = solrId.replace(pair[0], pair[1])

                    print(f"{datetime.now()} Solr ID: {solrId}")     
                
                #create the solr document
                content =[{
                        "id": solrId,
                        "content": full_text, 
                    }]
                
                
                solr.add(content)

        except Exception as ex:
            print(f'{datetime.now()} Error: {ex.args[0]}')

    def ProcessDID(self, file_path):

       #extract the text and send to solr
        try:
            print(f"{datetime.now()} Processing DID  {file_path}")
            
            #for did files, read all the text into a list of strings
            with open(file_path, 'r') as f:
                
                did_content = [line.strip().lower() for line in f.readlines()]

                #send the text to solr
                solr = pysolr.Solr(self.config['solrUrl']  , always_commit=True, timeout=10)
            
                solrId = file_path
                
                # replace the path with the network path
                for pair in self.config['path_replacement_pairs']:
                    solrId = solrId.replace(pair[0], pair[1])     
                
                    print(f"{datetime.now()} Solr ID: {solrId}")
                    
                #create the solr document
                content =[{
                        "id": solrId,
                        "didcontent": did_content, 
                    }]
                
                
                solr.add(content)

        except Exception as ex:
            print(f'{datetime.now()} Error: {ex.args[0]}')

    
