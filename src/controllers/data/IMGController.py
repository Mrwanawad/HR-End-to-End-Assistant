import os
from PIL import Image
import numpy as np
import base64
import io
import inspect
from fastapi import status, HTTPException, Response
from config.config import get_settings
from colorama import Fore
from ..DataController import DataController
from streamlit.runtime.uploaded_file_manager import UploadedFile
from fastapi import UploadFile

class IMGController( DataController ) :
    
    
    
    def __init__(self):
        pass
    

    def validate_image( self, img: UploadedFile | UploadFile ):
        img_size = self.get_file_size_in_MB(img)
        img_ext = self.get_file_type(img)

        if img_size > get_settings().IMAGE_MAX_SIZE:
            raise ValueError( 'Image Size should be lower than 10 MB' )
        
        if img_ext not in get_settings().IMAGES_ALLOWED_TYPES:
            raise ValueError( 'Image Extension Not Supported' )
        
        return True

    async def read_img_into_buffer(self, img: UploadedFile | UploadFile, img_size=(256, 256), quality: int = 85):
        valid = self.validate_image(img)
        
        # ✅ Handle both Streamlit (sync) and FastAPI (async) file reads
        if inspect.iscoroutinefunction(img.read):
            img_bytes = await img.read()  # FastAPI UploadFile
        else:
            img_bytes = img.read()        # Streamlit UploadedFile

        img_pil = Image.open(io.BytesIO(img_bytes))

        if valid:
            if img_pil.mode in ('RGBA', 'P'):
                img_pil = img_pil.convert('RGB')

            img_pil.thumbnail(img_size, Image.Resampling.LANCZOS)
            buffer = io.BytesIO()
            img_pil.save(buffer, format='JPEG', quality=quality)
            buffer.seek(0)
            return buffer.read()  
        
                
    async def load_img_into_base64_4_llm( self, img: Image.Image, img_size= (256, 256), quality: int = 85 ) -> str :
        
        """_summary_
            Take the image as a path or a PIL Object and returns the decoded version of it to directly send it to the LLM
        Returns:
            Image Data: Decoded Version of teh Image
        """
        img_data_in_buffer = await self.read_img_into_buffer( img )
        img_decoded = base64.b64encode( img_data_in_buffer ).decode( 'utf-8' ) 
        return img_decoded
                
             
               
               
if __name__ == "__main__":
    
    img_controller = IMGController()
    '''    img_data = img_controller.load_img_into_base64_4_llm( img = 'src/assets/test-cvs-imgs/cv4_computer_vision.png' )
    print( f'First 30 Chars. of the decoded image string: `{img_data[:30]}...................`' )
     
    print() '''
            
    pil_test_img_data = img_controller.load_img_into_base64_4_llm( img = 'src/assets/test-cvs-imgs/edge-cases/cv.'  ) # type:ignore
    print( f'First 30 Chars. of the decoded image string: `{pil_test_img_data[:30]}...................`' )
    
    

        