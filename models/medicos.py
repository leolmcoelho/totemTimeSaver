from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Medico(BaseModel):
    user_id:int = None
    name:str = None
    cpf:str = None
    conselho:str = None
    uf:str = None
    cbo:str = None
    registro:str = None
    