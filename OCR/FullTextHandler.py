
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os
import time
import pysolr

# This class handles the file system events for the folder being watched
class TextFileHandler(FileSystemEventHandler,):

    def __init__(self, folder_to_watch, solrUrl, path_replacement_pairs ):
        super().__init__()
        self.folder_to_watch = folder_to_watch
        self.solrUrl = solrUrl
        self.path_replacement_pairs = path_replacement_pairs
        self.running = True
    def on_created(self, event):
        try:
            if not event.is_directory: 
                
                if event.src_path.lower().endswith('.txt') :
                
                    file_path = event.src_path

                    # wait for the file to be fully written
                    file_size = -1
                    
                    while os.path.getsize(file_path) != file_size:
                        file_size = os.path.getsize(file_path)
                        time.sleep(5) # wait for 5 seconds
                    self.ProcessFullText(file_path)

                elif event.src_path.lower().endswith('.did') :
                    file_path = event.src_path
                    self.ProcessDID(file_path)

        except Exception as ex:
            print(f'{datetime.now()} Error: {str(ex)}')

    def on_modified(self, event):
        return self.on_created(event)
    
    
        
    def ProcessFullText(self, file_path):

       #extract the text and send to solr
        try:
            print(f"{datetime.now()} Processing TEXT  {file_path}")
            
            #for text files, read all the text into a string
            with open(file_path, 'r') as f:   #,encoding="utf8"
                full_text = f.read()

                #send the text to solr
                solr = pysolr.Solr(self.solrUrl  , always_commit=True, timeout=10)
                
                solrId = file_path
                
                # replace the path with the network path
                for pair in self.path_replacement_pairs:
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
                solr = pysolr.Solr(self.solrUrl  , always_commit=True, timeout=10)
            
                solrId = file_path
                
                # replace the path with the network path
                for pair in self.path_replacement_pairs:
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

    def ProcessALL(self):
        try:
            # To process all files in the folder (excluding subdirectories):
            folder_to_process = self.folder_to_watch  # Assuming you pass the folder path when creating the handler instance

            for root, _, files in os.walk(folder_to_process):
                    for filename in files:
                        if not self.running:
                                break
                        elif filename.lower().endswith('.txt'):
                            self.ProcessFullText(os.path.join(root,filename))
                        elif filename.lower().endswith('.did'):
                            self.ProcessDID(os.path.join(root,filename))

        except Exception as ex:
            print(f'{datetime.now()} Error: {str(ex)}')
            
    def stop(self):
        self.running = False