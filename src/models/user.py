from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel): 
    user:str = None
    password:str = None
    code: str = None 
    
    

class IStenci(BaseModel):    
    carteira:str = None
    medico:str = None
    convenio:str = None
    
    