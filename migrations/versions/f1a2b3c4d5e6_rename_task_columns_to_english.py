"""rename task columns to english

Revision ID: f1a2b3c4d5e6
Revises: 888a89d773d4
Create Date: 2025-12-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f1a2b3c4d5e6"
down_revision: Union[str, Sequence[str], None] = "888a89d773d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "task",
        "titulo",
        new_column_name="title",
        existing_type=sa.String(length=100),
        nullable=False,
    )
    op.alter_column(
        "task",
        "descripcion",
        new_column_name="description",
        existing_type=sa.String(length=255),
        nullable=True,
    )
    op.alter_column(
        "task",
        "estado",
        new_column_name="status",
        existing_type=sa.Enum("pending", "in_progress", "done", name="taskstatus"),
        nullable=False,
    )
    op.alter_column(
        "task",
        "fecha",
        new_column_name="created_at",
        existing_type=sa.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    # Nuevo índice para filtrar por estado con mejor rendimiento
    op.create_index("ix_task_status", "task", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_task_status", table_name="task")

    op.alter_column(
        "task",
        "created_at",
        new_column_name="fecha",
        existing_type=sa.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
    op.alter_column(
        "task",
        "status",
        new_column_name="estado",
        existing_type=sa.Enum("pending", "in_progress", "done", name="taskstatus"),
        nullable=False,
    )
    op.alter_column(
        "task",
        "description",
        new_column_name="descripcion",
        existing_type=sa.String(length=255),
        nullable=True,
    )
    op.alter_column(
        "task",
        "title",
        new_column_name="titulo",
        existing_type=sa.String(length=100),
        nullable=False,
    )
