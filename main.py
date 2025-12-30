from typing import List  # Tipado para listas en las respuestas

from fastapi import Depends, FastAPI, HTTPException, Query  # Importa FastAPI y utilidades de dependencias/errores
from sqlalchemy.orm import Session  # Proporciona el tipo de sesion de SQLAlchemy

from database import engine, get_db  # Engine de la base de datos y dependencia para obtener sesiones
from model import Base, Task, User  # Base ORM y modelos Task y User
from schemas import (
    TaskCreate, TaskRead, TaskUpdate, PaginatedTaskResponse,  # Esquemas de tareas
    UserCreate, UserRead, Token  # Esquemas de autenticacion
)
from auth import hash_password, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES  # Funciones de autenticacion
from datetime import timedelta  # Para calcular expiracion del token


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


@app.get("/tasks", response_model=PaginatedTaskResponse)  # Ruta GET para listar tareas con paginacion
def list_tasks(  # Funcion que lista tareas con soporte para paginacion
    page: int = 1,  # Numero de pagina (por defecto 1), minimo 1
    page_size: int = 10,  # Cantidad de items por pagina (por defecto 10), minimo 1
    db: Session = Depends(get_db)  # Sesion de BD inyectada
):  # Retorna respuesta paginada con metadata
    if page < 1:  # Valida que la pagina sea al menos 1
        page = 1  # Corrige a pagina 1 si es invalida
    if page_size < 1:  # Valida que page_size sea al menos 1
        page_size = 10  # Corrige a 10 si es invalido

    total = db.query(Task).count()  # Cuenta el total de tareas en la BD
    offset = (page - 1) * page_size  # Calcula el offset basado en pagina y tamaño
    tasks = db.query(Task).limit(page_size).offset(offset).all()  # Obtiene las tareas de la pagina actual
    total_pages = (total + page_size - 1) // page_size  # Calcula el total de paginas

    return {  # Retorna la respuesta con items y metadata de paginacion
        "items": tasks,  # Lista de tareas de la pagina actual
        "total": total,  # Total de tareas en la BD
        "page": page,  # Numero de pagina actual
        "page_size": page_size,  # Tamaño de pagina utilizado
        "total_pages": total_pages  # Total de paginas disponibles
    }


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


@app.delete("/tasks/{task_id}", status_code=204)  # Ruta DELETE para eliminar una tarea
def delete_task(task_id: int, db: Session = Depends(get_db)):  # Recibe el ID como parametro de ruta y la sesion
    task = db.query(Task).filter(Task.id == task_id).first()  # Busca la tarea por ID

    if not task:  # Si no existe la tarea
        raise HTTPException(status_code=404, detail="Tarea no encontrada")  # Lanza error 404

    db.delete(task)  # Marca la tarea para eliminar
    db.commit()  # Confirma la eliminacion en la base


# Endpoints de autenticación
@app.post("/register", response_model=UserRead, status_code=201)  # Ruta POST para registrar nuevo usuario
def register_user(user: UserCreate, db: Session = Depends(get_db)):  # Recibe datos de usuario y sesion
    """Crea un nuevo usuario con contraseña hasheada"""
    existing_user = db.query(User).filter(User.username == user.username).first()  # Verifica si el usuario ya existe
    if existing_user:  # Si ya existe un usuario con ese username
        raise HTTPException(status_code=400, detail="El usuario ya existe")  # Lanza error 400
    
    hashed_pwd = hash_password(user.password)  # Hashea la contraseña
    db_user = User(username=user.username, hashed_password=hashed_pwd)  # Crea instancia del usuario
    db.add(db_user)  # Agrega el usuario a la sesion
    db.commit()  # Confirma los cambios
    db.refresh(db_user)  # Refresca con datos de la BD
    return db_user  # Retorna el usuario creado (sin contraseña)


@app.post("/login", response_model=Token)  # Ruta POST para autenticar usuario
def login(user: UserCreate, db: Session = Depends(get_db)):  # Recibe credenciales y sesion
    """Autentica un usuario y retorna un token JWT"""
    db_user = db.query(User).filter(User.username == user.username).first()  # Busca el usuario
    if not db_user:  # Si no existe el usuario
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")  # Error 401
    
    if not verify_password(user.password, db_user.hashed_password):  # Verifica la contraseña
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")  # Error 401
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Define tiempo de expiracion
    access_token = create_access_token(  # Crea el token JWT
        data={"sub": db_user.username},  # Payload con el username
        expires_delta=access_token_expires  # Tiempo de expiracion
    )
    return {"access_token": access_token, "token_type": "bearer"}  # Retorna el token
