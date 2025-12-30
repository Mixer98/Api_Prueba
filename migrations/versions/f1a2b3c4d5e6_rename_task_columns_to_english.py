"""rename task columns to english

Revision ID: f1a2b3c4d5e6
Revises: 888a89d773d4
Create Date: 2025-12-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op  # Operaciones de migracion de Alembic
import sqlalchemy as sa  # Tipos de datos de SQLAlchemy

# revision identifiers, used by Alembic.
revision: str = "f1a2b3c4d5e6"  # ID unico de esta migracion
down_revision: Union[str, Sequence[str], None] = "888a89d773d4"  # Migracion anterior requerida
branch_labels: Union[str, Sequence[str], None] = None  # Etiquetas de rama (no usadas)
depends_on: Union[str, Sequence[str], None] = None  # Dependencias adicionales (ninguna)


def upgrade() -> None:
    """Renombra las columnas de la tabla task de español a inglés y agrega índice en status"""
    # Renombrar columna titulo a title (titulo obligatorio de la tarea)
    op.alter_column(
        "task",  # Tabla a modificar
        "titulo",  # Nombre actual de la columna
        new_column_name="title",  # Nuevo nombre en inglés
        existing_type=sa.String(length=100),  # Tipo actual de la columna
        nullable=False,  # Mantener como obligatoria
    )
    # Renombrar columna descripcion a description (descripción opcional de la tarea)
    op.alter_column(
        "task",  # Tabla a modificar
        "descripcion",  # Nombre actual de la columna
        new_column_name="description",  # Nuevo nombre en inglés
        existing_type=sa.String(length=255),  # Tipo actual de la columna
        nullable=True,  # Mantener como opcional
    )
    # Renombrar columna estado a status (estado de la tarea: pending/in_progress/done)
    op.alter_column(
        "task",  # Tabla a modificar
        "estado",  # Nombre actual de la columna
        new_column_name="status",  # Nuevo nombre en inglés
        existing_type=sa.Enum("pending", "in_progress", "done", name="taskstatus"),  # Tipo Enum con valores
        nullable=False,  # Mantener como obligatoria
    )
    # Renombrar columna fecha a created_at (timestamp de creación/actualización)
    op.alter_column(
        "task",  # Tabla a modificar
        "fecha",  # Nombre actual de la columna
        new_column_name="created_at",  # Nuevo nombre en inglés
        existing_type=sa.TIMESTAMP(),  # Tipo timestamp
        nullable=False,  # Mantener como obligatoria
        existing_server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),  # Mantener auto-actualización
    )

    # Crear índice en la columna status para mejorar el rendimiento en filtros por estado
    op.create_index("ix_task_status", "task", ["status"], unique=False)


def downgrade() -> None:
    """Revierte los cambios: elimina índice y renombra columnas de inglés a español"""
    # Eliminar el índice creado en status
    op.drop_index("ix_task_status", table_name="task")

    # Revertir created_at a fecha
    op.alter_column(
        "task",  # Tabla a modificar
        "created_at",  # Nombre actual en inglés
        new_column_name="fecha",  # Revertir a nombre en español
        existing_type=sa.TIMESTAMP(),  # Tipo timestamp
        nullable=False,  # Mantener como obligatoria
        existing_server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),  # Mantener auto-actualización
    )
    # Revertir status a estado
    op.alter_column(
        "task",  # Tabla a modificar
        "status",  # Nombre actual en inglés
        new_column_name="estado",  # Revertir a nombre en español
        existing_type=sa.Enum("pending", "in_progress", "done", name="taskstatus"),  # Tipo Enum con valores
        nullable=False,  # Mantener como obligatoria
    )
    # Revertir description a descripcion
    op.alter_column(
        "task",  # Tabla a modificar
        "description",  # Nombre actual en inglés
        new_column_name="descripcion",  # Revertir a nombre en español
        existing_type=sa.String(length=255),  # Tipo string
        nullable=True,  # Mantener como opcional
    )
    # Revertir title a titulo
    op.alter_column(
        "task",  # Tabla a modificar
        "title",  # Nombre actual en inglés
        new_column_name="titulo",  # Revertir a nombre en español
        existing_type=sa.String(length=100),  # Tipo string
        nullable=False,  # Mantener como obligatoria
    )
