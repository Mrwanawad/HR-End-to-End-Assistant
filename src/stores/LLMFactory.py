from config.config import get_settings
from stores.providers.MistralProvider import MistralAIProvider
from stores.providers.OllamaProvider import OllamaProvider
from stores.providers.GroqProvider import GroqProvider

settings = get_settings()

class LLMFactory:
    
    
    def __init__(self):
        pass
    
    def return_provider( self ):
        
        provider = settings.LLM_PROVIDER
        if provider == 'ollama':
            return OllamaProvider( model= settings.OLLAMA_MODEL )
        
        elif provider == 'mistral':
            return MistralAIProvider( api_key= settings.MISTRAL_API_KEY, model_id= settings.MISTRAL_MODEL )
        
        elif provider == 'groq':
            return GroqProvider( api_key= settings.GROQ_API_KEY, model_id= settings.GROQ_MODEL )
        
        
                
    
    