from datetime import datetime  # Marca de tiempo de creacion/actualizacion
from enum import Enum  # Enum base de Python
from typing import List, Optional  # Tipado opcional para campos no requeridos y listas

from pydantic import BaseModel, ConfigDict, constr  # Base, configuracion y restricciones de campos


class TaskStatus(str, Enum):  # Estados posibles de una tarea
    pending = "pending"  # Tarea creada pero no iniciada
    in_progress = "in_progress"  # Tarea en curso
    done = "done"  # Tarea finalizada


class TaskBase(BaseModel):  # Campos compartidos entre creacion y lectura
    titulo: str  # Titulo obligatorio
    descripcion: Optional[str] = None  # Descripcion opcional
    estado: TaskStatus = TaskStatus.pending  # Estado con valor por defecto


class TaskCreate(TaskBase):  # Esquema para crear tareas
    pass  # No agrega campos nuevos


class TaskRead(TaskBase):  # Esquema para leer tareas
    id: int  # Identificador de la tarea
    fecha: datetime  # Fecha/hora asignada por la BD

    model_config = ConfigDict(from_attributes=True)  # Permite leer desde objetos ORM en Pydantic v2


class TaskUpdate(BaseModel):  # Esquema para actualizar tareas parcialmente
    titulo: Optional[str] = None  # Titulo opcional para actualizar
    descripcion: Optional[str] = None  # Descripcion opcional para actualizar
    estado: Optional[TaskStatus] = None  # Estado opcional para actualizar


class PaginatedTaskResponse(BaseModel):  # Esquema de respuesta paginada
    items: List[TaskRead]  # Lista de tareas en la pagina actual
    total: int  # Total de tareas en la BD
    page: int  # Numero de pagina actual
    page_size: int  # Cantidad de items por pagina
    total_pages: int  # Total de paginas disponibles


# Schemas de autenticación
class UserCreate(BaseModel):  # Esquema para registrar un nuevo usuario
    username: constr(min_length=3, max_length=50)  # pyright: ignore[reportInvalidTypeForm] # Nombre de usuario con longitud acotada
    password: constr(min_length=6, max_length=72)  # type: ignore # Contraseña acotada para bcrypt (72 bytes máx)


class UserRead(BaseModel):  # Esquema para leer datos de usuario (sin contraseña)
    id: int  # ID del usuario
    username: str  # Nombre de usuario

    model_config = ConfigDict(from_attributes=True)  # Permite leer desde objetos ORM


class Token(BaseModel):  # Esquema de respuesta al hacer login
    access_token: str  # Token JWT generado
    token_type: str  # Tipo de token (siempre "bearer")
