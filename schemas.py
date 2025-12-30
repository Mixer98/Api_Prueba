from datetime import datetime  # Marca de tiempo de creacion/actualizacion
from enum import Enum  # Enum base de Python
from typing import Optional  # Tipado opcional para campos no requeridos

from pydantic import BaseModel, ConfigDict  # Base y configuracion para esquemas de validacion


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
