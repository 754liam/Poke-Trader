# Add currency and pricing fields to cards and collection items
# Alembic, SQLAlchemy

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = 'add_currency_pricing'
down_revision = '86c551ed8e16'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('user', sa.Column('balance', sa.Integer(), nullable=False, server_default='1000'))
    op.add_column('card', sa.Column('price', sa.Integer(), nullable=False, server_default='100'))
    op.add_column('card', sa.Column('last_price_update', sa.Date(), nullable=True))
    op.add_column('trade', sa.Column('message', sa.Text(), nullable=True))
    op.add_column('trade', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_table('requested_card', sa.Column('id', sa.Integer(), nullable=False), sa.Column('trade_id', sa.Integer(), nullable=False), sa.Column('collection_item_id', sa.Integer(), nullable=False), sa.Column('requesting_user_id', sa.Integer(), nullable=False), sa.ForeignKeyConstraint(['collection_item_id'], ['collection_item.id']), sa.ForeignKeyConstraint(['requesting_user_id'], ['user.id']), sa.ForeignKeyConstraint(['trade_id'], ['trade.id']), sa.PrimaryKeyConstraint('id'))

def downgrade():
    op.drop_table('requested_card')
    op.drop_column('trade', 'updated_at')
    op.drop_column('trade', 'message')
    op.drop_column('card', 'last_price_update')
    op.drop_column('card', 'price')
    op.drop_column('user', 'balance')