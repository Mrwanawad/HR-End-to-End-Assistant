import os
from config.config import get_settings
from typing import Literal
from streamlit.runtime.uploaded_file_manager import UploadedFile
from fastapi import UploadFile



class DataController:
    
    def __init__(self):
        pass
    
    def get_file_size_in_MB( self, doc: UploadedFile | UploadFile ):
        if hasattr( doc, 'size' ):
            size_in_mb = doc.size / ( 1024 * 1024 )
            
        else:
            doc.file.seek( 0, 2 )
            size_in_bytes = doc.file.tell() 
            doc.file.seek(0)             
            size_in_mb = size_in_bytes / (1024 * 1024)
            
        return size_in_mb        
    
    def get_file_type( self, file: UploadedFile | UploadFile ):
        
        file_type = file.type if isinstance( file, UploadedFile ) else file.content_type

        return file_type        
    
    
    def get_data_type(self, file: UploadedFile | UploadFile ): 
        
        file_type = self.get_file_type( file )
        
        if file_type in get_settings().IMAGES_ALLOWED_TYPES:
            return 'img'
            
        elif file_type in get_settings().FILE_ALLOWED_TYPES:
            return 'doc'
            
        else: 
            return None


            
                