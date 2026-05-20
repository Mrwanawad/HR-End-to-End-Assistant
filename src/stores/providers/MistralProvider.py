import os
import sys;                                                         
from stores.providers.ProviderInterface import LLMInterface
from mistralai.client import Mistral
from config.config import get_settings
from colorama import Fore
from typing import List
from models import UserEntries
from schemas import build_img_messages_schema

class MistralAIProvider( LLMInterface ):
    
    def __init__(self, api_key: str, model_id: str, input_max_chars: int = 1000, output_max_chars: int = 1000, ):
        self.api_key = api_key
        self.model_id = model_id
        self.client = Mistral( api_key= self.api_key )
        self.input_max_chars = input_max_chars
        self.output_max_chars = output_max_chars
        
    def set_generation_model(self, model_id):
        self.model_id = model_id
        
    def generate_text( self, system_prompt: str, user_prompt: str, max_output_tokens: int = 2048, temp: float = 0.0) : # type: ignore
        
        messages =  [
            { 'role': 'system', 'content': system_prompt },
            { 'role': 'user', 'content': user_prompt }
        ]    
        response = self.client.chat.complete( model= self.model_id, messages= messages,                 # type: ignore
                                             max_tokens= max_output_tokens, temperature= temp )   

        return response.choices[0].message.content                                                      # type: ignore
                
    def analyze_cv( self, messages: List, max_output_tokens: int = 2048, temp: float = 0.0 )  :         # type: ignore
        response = self.client.chat.complete(
            model= self.model_id,
            messages= messages,
            max_tokens= max_output_tokens,
            temperature= temp
        )
        json_response = self.parse_json( response.choices[0].message.content )
        
        return json_response              # type: ignore       
                


if __name__ == '__main__':
    
    mistral_clent = MistralAIProvider(
        api_key= get_settings().MISTRAL_API_KEY,
        model_id= get_settings().MISTRAL_MODEL
    )   
    
    if not mistral_clent.api_key:
        raise ValueError( 'API Key Not Set !' )
    
    generated_text = mistral_clent.generate_text(
        system_prompt = 'Just Answer user QS !',
        user_prompt= "Where's Alexandria Located ?"
    ) 
    
    print( Fore.GREEN + f'Mistral Response: {generated_text}' + Fore.RESET )