"""Add cascade delete relationships

Revision ID: 1a31ce608336
Revises: d98dd8ec85a3

"""
from alembic import op # type: ignore
import sqlalchemy as sa # type: ignore
import sqlmodel.sql.sqltypes # type: ignore

revision = '1a31ce608336'
down_revision = 'd98dd8ec85a3'
branch_labels = None
depends_on = None

def upgrade():
   
    op.alter_column('item', 'owner_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint('item_owner_id_fkey', 'item', type_='foreignkey')
    op.create_foreign_key(None, 'item', 'user', ['owner_id'], ['id'], ondelete='CASCADE')
   
def downgrade():
   
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.create_foreign_key('item_owner_id_fkey', 'item', 'user', ['owner_id'], ['id'])
    op.alter_column('item', 'owner_id',
               existing_type=sa.UUID(),
               nullable=True)
    
