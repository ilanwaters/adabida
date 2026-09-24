"""visible_public de membres per defecte false

Revision ID: 708ace342adb
Revises: 9e56e0ff8a0a
Create Date: 2026-09-24 11:03:44.253529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '708ace342adb'
down_revision = '9e56e0ff8a0a'
branch_labels = None
depends_on = None


def upgrade():
    # Nous membres: ocults per defecte a nivell de BD
    op.alter_column(
        'membres_familia', 'visible_public',
        existing_type=sa.Boolean(),
        existing_nullable=False,
        server_default=sa.false(),
    )
    # Membres existents: cap estava triat conscientment
    op.execute("UPDATE membres_familia SET visible_public = FALSE")


def downgrade():
    op.alter_column(
        'membres_familia', 'visible_public',
        existing_type=sa.Boolean(),
        existing_nullable=False,
        server_default=None,
    )