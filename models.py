from pydantic import BaseModel

from typing import Optional

class Cantor (BaseModel):
    id: Optional[int] = None
    nome: str
    ano_nasc: int
    genero:str
    tempo_carreira: int



    