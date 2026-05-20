import os
import sys;
from typing import List
from models import UserEntries, LLMCandidateResponse
from schemas import build_img_messages_schema                                            
from stores.providers.ProviderInterface import LLMInterface
import ollama
from config.config import get_settings
from colorama import Fore

class OllamaProvider( LLMInterface ):
    
    def __init__(self, model: str):
        self.model= model
    
    def set_generation_model( self, model_id: str ):
        pass
    
    def generate_text( self, system_prompt: str, user_prompt: str, max_output_tokens: int = 2048, temp: float = 0.0 )  :
        messages =  [
            { 'role': 'system', 'content': system_prompt },
            { 'role': 'user', 'content': user_prompt }
        ]    
        response = ollama.chat( model= self.model, messages= messages,                 # type: ignore
                                options= {
                                   'num_ctx': max_output_tokens,
                                   'temperature': temp
                               }
                                 )   

        return response.message.content   
    
    
    def analyze_cv(self, messages: List, max_output_tokens: int = 2048, temp: float = 0.0):
        stream = ollama.chat(
            model=self.model,
            messages=messages,
            options={
                'num_ctx': max_output_tokens,
                'temperature': temp
            },
            stream=True
        )

        def response_generator():
            for chunk in stream:
                if chunk.message.content:
                    yield chunk.message.content

        return response_generator()
                

if __name__ == '__main__':
    ollama_model = OllamaProvider( 'gemma3' )
    response= ollama_model.generate_text( 'Help Users', 'Are You good at generating structured JSON repsonses ?' )
    print( Fore.GREEN + f'Ollama Response: {response}' + Fore.RESET  )
    