from pydantic import BaseModel, Field
from typing import Literal, List

class UserEntries( BaseModel ):
    
    seniority: str = Field(
        ...,
        examples= [ 'Entry-Level', 'Junior', 'Mid-Level', 'Senior', 'Team Lead/Head' ],
        description= 'The Seniority of the candidate'
    )
    years_of_exp: int = Field( ..., ge= 0, lt= 20, description= 'The No. indicating the candidate years of experience.' )
    job_role: str
    required_skills: List[ str ]
    job_description: str
    
    
if __name__ == '__main__':
    print( UserEntries.model_fields['seniority'].examples)
    #print( f'Model Schema:\n{UserEntries.model_json_schema()}' )    