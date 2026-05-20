import os
from fastapi import APIRouter, UploadFile, Depends, status
from fastapi.responses import JSONResponse
from config.config import get_settings
from models import UserEntries, LLMCandidateResponse
from controllers import DataController, IMGController, PDFController
from stores.LLMFactory import LLMFactory
from schemas import build_img_messages_schema, build_pdf_messages_schema
from json_repair import loads

data_router = APIRouter(
    prefix= '/api/v1',
    tags = [ 'api_v1' ]
)

llm_client = LLMFactory().return_provider()

@data_router.post( '/analyze' )
async def analyze_cv( user_entries: str, file: UploadFile, app_settings= Depends( get_settings ) ):
    
    try:
        user_entries = loads( user_entries )
    except Exception as e:
        return JSONResponse(
            content= f'Invalid User Entries Format',
            status_code= status.HTTP_400_BAD_REQUEST
        )
    
    file_type = DataController().get_data_type( file )
    
    if not file_type:
        return JSONResponse(
            content= 'File Extension is not Supported !',
            status_code= status.HTTP_400_BAD_REQUEST
        )
        
    user_entries = UserEntries( **user_entries )    
    
    if file_type == 'doc':
        messages = await build_pdf_messages_schema( file= file,
                                  user_entries= user_entries,)
        response = await llm_client.analyze_cv(
            messages = messages
        )
        
        return {
            'Analyzed CV': response
        }

    elif file_type == 'img':
        messages = await build_img_messages_schema( img= file, user_entries= user_entries )
        response = await llm_client.analyze_cv( messages= messages )
        return {
            'Analyzed CV': response
        }        
    
    
    
    
      