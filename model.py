
from sqlalchemy.sql import  func  # Importa funciones SQL como current_timestamp

from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP  # Importa tipos/columnas de SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base  # Permite declarar clases ORM
import enum  # Proporciona soporte para enumeraciones en Python

Base = declarative_base()  # Clase base que usarán todos los modelos ORM

class TaskStatus(enum.Enum):  # Enumeración para los posibles estados de una tarea
    pending = "pending"  # Tarea creada pero sin iniciar
    in_progress = "in_progress"  # Tarea en curso
    done = "done"  # Tarea finalizada

class Task(Base):  # Modelo ORM que representa la tabla "task"
    __tablename__ = "task"  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Clave primaria autoincremental
    titulo = Column(String(255), nullable=False)  # Título obligatorio de la tarea
    descripcion = Column(String(255))  # Descripción opcional
    estado = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.pending)  # Estado usando la enumeración
    fecha = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())  # Marca temporal de creación/actualización
