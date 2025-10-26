"""agregar campos requisitos y estado a eventos

Revision ID: add_requisitos_estado
Revises: 183f0eadc546
Create Date: 2024-03-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_requisitos_estado'
down_revision = '183f0eadc546'
branch_labels = None
depends_on = None


def upgrade():
    # Agregar columna requisitos
    op.add_column('eventos', sa.Column('requisitos', sa.Text(), nullable=True))
    
    # Agregar columna estado con valor por defecto 'pendiente'
    op.add_column('eventos', sa.Column('estado', sa.String(50), nullable=True, server_default='pendiente'))


def downgrade():
    # Eliminar las columnas en orden inverso
    op.drop_column('eventos', 'estado')
    op.drop_column('eventos', 'requisitos') 