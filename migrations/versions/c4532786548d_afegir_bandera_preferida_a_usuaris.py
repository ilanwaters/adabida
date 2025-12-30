"""Afegir bandera_preferida a usuaris

Revision ID: c4532786548d
Revises: f4ada394ea9e
Create Date: 2025-12-21 20:51:45.506161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4532786548d'
down_revision = 'f4ada394ea9e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('usuaris', sa.Column('bandera_preferida', sa.String(5), nullable=True))


def downgrade():
    op.drop_column('usuaris', 'bandera_preferida')
