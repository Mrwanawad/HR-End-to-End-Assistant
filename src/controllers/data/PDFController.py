import os
from config.config import get_settings
import pymupdf4llm 
import fitz  
import asyncio
from ..DataController import DataController
from streamlit.runtime.uploaded_file_manager import UploadedFile
from fastapi import UploadFile, responses, status
import re

class PDFController( DataController ):
    
    def __init__(self):
        pass
    
    def get_doc_size_in_MB( self, doc: UploadedFile | UploadFile ):
        if hasattr( doc, 'size' ):
            size_in_mb = doc.size / ( 1024 * 1024 )
            
        else:
            doc.file.seek( 0, 2 )
            size_in_bytes = doc.file.tell() 
            doc.file.seek(0)             
            size_in_mb = size_in_bytes / (1024 * 1024)
            
        return size_in_mb        
    

    
    def validate_doc(self, doc: UploadedFile | UploadFile) :
        
        doc_size = self.get_doc_size_in_MB( doc= doc )
        doc_type = self.get_file_type( file= doc )
        
        if doc_size > 10:
            return responses.JSONResponse(
                content= 'File Size is greater than 10 MB',
                status_code= status.HTTP_400_BAD_REQUEST
            )
        
        if doc_type not in get_settings().FILE_ALLOWED_TYPES:
            return responses.JSONResponse(
                content= f'File Extension not Supported !\nExtensions Supported: { get_settings().FILE_ALLOWED_TYPES }',
                status_code= status.HTTP_400_BAD_REQUEST
            )  
            
        return True
    
    def clean_processed_text( self, doc_text: str ):
        doc_text = re.sub(r'\n{3,}', '\n\n', doc_text)  # collapse excessive newlines
        doc_text = re.sub(r'[ \t]+', ' ', doc_text)      # collapse spaces/tabs
        doc_text = doc_text.strip()
        return doc_text


    
    async def process_doc(self, doc: UploadedFile | UploadFile):
        if self.validate_doc(doc=doc):
            
            # Handle both sync (Streamlit) and async (FastAPI) file reads
            if hasattr(doc, 'read'):
                result = doc.read()
                doc_bytes = await result if asyncio.iscoroutine(result) else result
            
            doc = fitz.open(stream=doc_bytes, filetype=f"{self.get_file_type(doc).split('/')[-1]}")
            
            doc_text = ""
            for page in doc:
                doc_text += page.get_text()
            
            return self.clean_processed_text(doc_text)
        
       
if __name__ == '__main__':
    ...               
        
        
        