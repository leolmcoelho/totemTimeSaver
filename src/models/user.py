from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel): 
    user:str = None
    password:str = None
    code: str = None 
    
    
class Medico(BaseModel):
    user_id:int = None
    name:str = None
    cpf:str = None
    conselho:str = None
    uf:str = None
    cbo:str = None
    registro:str = None
    
class IStenci(BaseModel):    
    carteira:str = None
    medico:str = None
    convenio:str = None
    
    