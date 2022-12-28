from fastapi import FastAPI
from fastapi import HTTPException, status, Response, Path, Query, Header, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List, Any, Dict
from time import sleep

from models import Curso

#Parametros para personalizar o /Docs
app = FastAPI(
    title='API padrão Fast API',
    version='0.0.1',
    description='Uma API para estudo do FastAPI'
)

#Simula conexão com um banco qualquer
def fake_db():
    try:
        print('Abrindo conexão')
        sleep(1)
    finally:
        print('fechando conexão')
        sleep(1)

cursos ={
    1:{
        "titulo": "Prog em c",
        "aulas": 47,
        "horas": 8
    },
    2:{
        "titulo": "Prog logica 2",
        "aulas": 87,
        "horas": 57
    }
}


@app.get('/cursos', 
        description='Retorna todos os cursos ou uma lista vazia',   #Mais parametros para personalizar o /Docs
        summary='Retorna todos os cursos',
        response_model=Dict[int, Curso],
        response_description='Sucesso!') 
async def get_cursos(db: Any = Depends(fake_db)): #Injeção de dependencias
    return cursos

@app.get('/curso/{curso_id}')
async def get_curso(curso_id: int = Path(default=None, title='ID do curso', description='Deve ser entre 1 e 3', gt=0, lt=3), db: Any = Depends(fake_db)): #PATH parameters server para limitar as informações no path
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.') #Trata a exceção

@app.post('/cursos', status_code=status.HTTP_201_CREATED, response_model=Curso)
async def post_curso(curso: Curso, db: Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    '''curso.id = next_id
    cursos.append(curso)'''
    cursos[next_id] = curso
    del curso.id
    return curso

@app.put('/curso/{curso_id}')
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado {curso_id}") 

@app.delete('/curso/{curso_id}')
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id]
        #return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content= curso_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não encontrado {curso_id}")


#Exemplo QUERY parameters e HEAD parameters
@app.get('/calculadora')
async def calculadora(a: int = Query(default=None, gt= 5), b: int = Query(default=None, gt= 10), x_geek: str = Header(default=None) , c: Optional[int]= None):
    soma = a + b
    if c:
        soma = soma + c
    
    print(f'X_GEEK: {x_geek}')

    return {"Resultado": soma}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, 
                 reload=True)