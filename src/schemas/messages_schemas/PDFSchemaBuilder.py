from PIL import Image
from schemas import SYSTEM_PROMPT
from models import UserEntries
from controllers.data.PDFController import PDFController


async def build_pdf_messages_schema( file, user_entries: UserEntries, provider: str ):

    pdf_text = await PDFController().process_doc( file )
    
    messages= [
        
        {
            'role': 'system',
            'content': SYSTEM_PROMPT
        },
        
        {
            'role': 'user',
            'content': '\n'.join([
                f'User Entries:\n{user_entries.model_dump_json()}',
                f'CV Content: {pdf_text}'
            ])
        }
        
    ]
    
    return messages


