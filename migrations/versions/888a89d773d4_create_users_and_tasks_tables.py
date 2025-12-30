"""Create users and tasks tables

Revision ID: 888a89d773d4
Revises: 
Create Date: 2025-12-30 13:56:15.023627

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from passlib.context import CryptContext  # Para hashear la contraseña del usuario inicial

# revision identifiers, used by Alembic.
revision: str = '888a89d773d4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    """Upgrade schema."""
    # Crear tabla users
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    
    # Crear tabla tasks
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=100), nullable=False),
    sa.Column('descripcion', sa.String(length=255), nullable=True),
    sa.Column('estado', sa.Enum('pending', 'in_progress', 'done', name='taskstatus'), nullable=False),
    sa.Column('fecha', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_id'), 'task', ['id'], unique=False)
    
    # Seed: Crear usuario admin automáticamente
    from sqlalchemy.orm import Session
    from model import User

    # Obtener la conexión de la migración
    bind = op.get_bind()
    session = Session(bind=bind)

    # Verificar si el usuario admin ya existe
    admin_exists = session.query(User).filter(User.username == "admin").first()

    if not admin_exists:
        # Hashear la contraseña
        hashed_pwd = pwd_context.hash("admin123")

        # Crear usuario admin
        admin_user = User(
            username="admin",
            hashed_password=hashed_pwd
        )
        session.add(admin_user)
        session.commit()

    session.close()


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar índices y tablas
    op.drop_index(op.f('ix_task_id'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
