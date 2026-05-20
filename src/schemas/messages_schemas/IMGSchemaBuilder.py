from config.config import get_settings
from PIL import Image
from controllers.data.IMGController import IMGController
from schemas import SYSTEM_PROMPT
from models import UserEntries
import ollama


async def build_img_messages_schema( img, user_entries: UserEntries, provider: str = get_settings().LLM_PROVIDER ):
    
    
    if provider == 'ollama':
        response = ollama.chat(
        model='gemma3',
        messages=[
            
            {
            'role': 'system',
            'content': SYSTEM_PROMPT
            },
            
            {
                'role': 'user',
                'content': f'User Entries:\n{user_entries.model_dump_json()}' ,
                'images': [img.read()]  # pass raw bytes here
            }
        ]
        )
        return response.message.content

    elif provider == 'mistral':
        decoded_img = await IMGController().load_img_into_base64_4_llm( img = img )
        
        messages = [
            
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            
            { 
                'role': 'user',
                'content': [
                    { 'type': 'image_url', 'image_url': f'data:image/jpeg;base64,{decoded_img}' },
                    { 'type': 'text', 'text': f'User Entries:\n{user_entries.model_dump_json()}' }
                ]
            }
            
        ]
        
        return messages
    
    elif provider == 'groq':
        
        decoded_img = await IMGController().load_img_into_base64_4_llm( img = img )
        messages = messages = [                          
            {                                
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {                                 
                "role": "user",
                "content": [
                    {"type": "text", "text": f'User Entries:\n{user_entries.model_dump_json()}'},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{decoded_img}"
                        }
                    },
                ],
            },
        ]                                   
        return messages