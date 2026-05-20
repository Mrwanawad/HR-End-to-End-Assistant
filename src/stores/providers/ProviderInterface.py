from abc import ABC, abstractmethod
from typing import List
from PIL import Image
from models import UserEntries
import json_repair;                 




class LLMInterface( ABC ):
    
    @abstractmethod
    def set_generation_model( self, model_id: str ):
        pass
    
    @abstractmethod
    def generate_text( self, system_prompt: str, user_prompt: str, max_output_tokens: int = 2048, temp: float = 0.0 )  :
        pass
    
    
    @abstractmethod 
    def analyze_cv( self, messages: List, max_output_tokens: int = 2048, temp: float = 0.0 )  :
        pass
    
    @staticmethod
    def parse_json(text):
        try:            return json_repair.loads( text )
        except:         return None
    
    