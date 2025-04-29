
from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI() #Inicializamos variable para traer las caracteristicas de API REST

class Curso(BaseModel): # Definimos el modelo
    id : Optional[str] = None
    nombre: str
    descripcion: Optional[str]=None
    nivel :str
    duracion: int

#simulamos una base de datos, se usa una lista como base de datos
cursos_db=[]

# CRUD: Read (lectura) GET ALL : leemos todos los cursos que hay en la base de datos db

@app.get("/cursos/",response_model= List[Curso])
def obtener_cursos():
    return cursos_db


# CRUD: create (escribir) POST : agregaremos un nuevo recurso a la base de datos db
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4())  #agregamos id unico con generador automatico
    cursos_db.append(curso)
    return curso

# CRUD : Read (lectura) GET (individual): Leemos el curso que coincida con el id que se pida
@app.get("/cursos/{curso_id}",response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None) #con next tomamos la primera coincidencia del arreglo
    if curso is None:
       raise HTTPException(status_code=404, detail="Curso NO ENCONTRADO")
    return curso


# CRUD : Update (Actualizar o modificar) PUT: Modificamos el curso que coincida con el id que se pida
@app.put("/cursos/{curso_id}",response_model=Curso)
def actualizar_curso(curso_id:str , curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso NO ENCONTRADO")
    curso_actualizado.id= curso_id
    index = cursos_db.index(curso) #se busca el indice donde esta el curso
    cursos_db[index]= curso_actualizado
    return curso_actualizado

# CRUD Delete (eliminar) DELETE : eliminamos el curso que coincida con el id que enviemos

@app.delete("/cursos/{curso_id}",response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id),None) #con next tomamos la primera coincidencia del arreglo
    if curso is None:
       raise HTTPException(status_code=404, detail="Curso NO ENCONTRADO")
    cursos_db.remove(curso)
    return curso