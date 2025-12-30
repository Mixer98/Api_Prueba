from typing import List  # Tipado para listas en las respuestas

from fastapi import Depends, FastAPI, HTTPException  # Importa FastAPI y utilidades de dependencias/errores
from sqlalchemy.orm import Session  # Proporciona el tipo de sesion de SQLAlchemy

from database import engine, get_db  # Engine de la base de datos y dependencia para obtener sesiones
from model import Base, Task  # Base ORM y modelo Task
from schemas import TaskCreate, TaskRead, TaskUpdate  # Esquemas de entrada y salida


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


@app.get("/tasks/{task_id}", response_model=TaskRead)  # Ruta GET para obtener una tarea por ID
def get_task(task_id: int, db: Session = Depends(get_db)):  # Recibe el ID como parametro de ruta y la sesion
    task = db.query(Task).filter(Task.id == task_id).first()  # Busca la tarea por ID
    if not task:  # Si no existe la tarea
        raise HTTPException(status_code=404, detail="Tarea no encontrada")  # Lanza error 404
    return task  # Devuelve la tarea encontrada


@app.put("/tasks/{task_id}", response_model=TaskRead)  # Ruta PUT para actualizar una tarea
def update_task(
    task_id: int,  # ID de la tarea a actualizar
    task_data: TaskUpdate,  # Datos validados con campos opcionales
    db: Session = Depends(get_db)  # Sesion de BD inyectada
):  # Funcion que actualiza parcialmente una tarea
    task = db.query(Task).filter(Task.id == task_id).first()  # Busca la tarea por ID

    if not task:  # Si no existe la tarea
        raise HTTPException(status_code=404, detail="Tarea no encontrada")  # Lanza error 404

    for field, value in task_data.dict(exclude_unset=True).items():  # Itera solo campos enviados
        setattr(task, field, value)  # Actualiza cada campo en la instancia ORM

    db.commit()  # Confirma los cambios en la base
    db.refresh(task)  # Refresca la instancia con datos persistidos
    return task  # Devuelve la tarea actualizada
