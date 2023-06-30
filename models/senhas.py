from pydantic import BaseModel
from typing import Optional

class Empresa(BaseModel):
    empresa_name: str
    user: str
    password: str
    code: Optional[str]

class SenhasResponse(BaseModel):
    result: list[Empresa]