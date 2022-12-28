from typing import Optional

from pydantic import BaseModel, validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

'''
    @validator('titulo')
    def validator_titulo(cls, value: str):
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O titulo deve ter pelo menos 3 palavras')
        
        return value


cursos = [
    Curso(id=1,titulo='Prog Leigos A', aulas= 112, horas=58),
    Curso(id=2,titulo='Prog Logica B', aulas= 87, horas=41),
]
'''