from typing import List  # Tipado para listas en las respuestas

from fastapi import Depends, FastAPI  # Importa FastAPI y utilidades de dependencias
from sqlalchemy.orm import Session  # Proporciona el tipo de sesion de SQLAlchemy

from database import engine, get_db  # Engine de la base de datos y dependencia para obtener sesiones
from model import Base, Task  # Base ORM y modelo Task
from schemas import TaskCreate, TaskRead  # Esquemas de entrada y salida


app = FastAPI()  # Instancia principal de la aplicacion FastAPI


@app.on_event("startup")  # Ejecuta la funcion al iniciar la app
def on_startup():  # Define la funcion de arranque
    try:  # Intenta crear las tablas
        Base.metadata.create_all(bind=engine)  # Crea tablas segun los modelos
    except Exception as exc:  # Captura cualquier error
        print(f"Error creando tablas: {exc}")  # Imprime el error para depurar


@app.get("/")  # Ruta GET para la raiz
def root():  # Funcion que maneja la raiz
    return {"message": "API funcionando"}  # Respuesta simple de estado


@app.post("/tasks", response_model=TaskRead)  # Ruta POST para crear tareas
def create_task(task: TaskCreate, db: Session = Depends(get_db)):  # Recibe datos validados y sesion inyectada
    db_task = Task(**task.dict())  # Crea instancia ORM con los datos recibidos
    db.add(db_task)  # Agrega la tarea a la sesion
    db.commit()  # Confirma los cambios en la base
    db.refresh(db_task)  # Refresca la instancia con datos persistidos
    return db_task  # Devuelve la tarea creada


@app.get("/tasks", response_model=List[TaskRead])  # Ruta GET para listar todas las tareas
def list_tasks(db: Session = Depends(get_db)):  # Inyecta sesion de BD para la consulta
    tasks = db.query(Task).all()  # Obtiene todas las tareas almacenadas
    return tasks  # Devuelve la lista de tareas
