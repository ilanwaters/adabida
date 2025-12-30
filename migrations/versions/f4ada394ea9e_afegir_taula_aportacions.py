"""Afegir taula aportacions

Revision ID: f4ada394ea9e
Revises: ac185fac63e3
Create Date: 2025-12-20 22:13:28.439593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4ada394ea9e'
down_revision = 'ac185fac63e3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('aportacions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuari_id', sa.Integer(), nullable=True),
    sa.Column('quantitat', sa.Numeric(10, 2), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('metode_pagament', sa.String(50), nullable=True),
    sa.Column('estat', sa.String(20), nullable=False, server_default='confirmada'),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('pais', sa.String(100), nullable=True),
    sa.Column('referit_per', sa.Integer(), nullable=True),
    sa.Column('comissio_percentatge', sa.Numeric(5, 2), nullable=True),
    sa.Column('comissio_pagada', sa.Boolean(), nullable=False, server_default='0'),
    sa.ForeignKeyConstraint(['usuari_id'], ['usuaris.id'], ),
    sa.ForeignKeyConstraint(['referit_per'], ['usuaris.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('aportacions')