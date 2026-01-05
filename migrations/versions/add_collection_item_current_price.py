# Add current price tracking to collection items
# Alembic, SQLAlchemy

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select
revision = 'add_coll_item_current_price'
down_revision = 'add_purchase_price'
branch_labels = None
depends_on = None
CONDITION_MULTIPLIERS = {'Near Mint': 1.0, 'Lightly Played': 0.8, 'Moderately Played': 0.64, 'Heavily Played': 0.512, 'Damaged': 0.4096}

def upgrade():
    op.add_column('collection_item', sa.Column('current_price', sa.Integer(), nullable=True))
    bind = op.get_bind()
    collection_item = table('collection_item', column('id', sa.Integer), column('card_id', sa.Integer), column('condition', sa.String), column('purchase_price', sa.Integer), column('current_price', sa.Integer))
    card = table('card', column('id', sa.Integer), column('price', sa.Integer))
    join_stmt = collection_item.join(card, collection_item.c.card_id == card.c.id)
    rows = bind.execute(select(collection_item.c.id, collection_item.c.condition, collection_item.c.purchase_price, card.c.price).select_from(join_stmt)).fetchall()
    for row in rows:
        if row.purchase_price and row.purchase_price > 0:
            current_price = row.purchase_price
        else:
            base_price = row.price or 100
            multiplier = CONDITION_MULTIPLIERS.get(row.condition, 1.0)
            current_price = max(1, int(base_price * multiplier))
        bind.execute(collection_item.update().where(collection_item.c.id == row.id).values(current_price=current_price))
    op.alter_column('collection_item', 'current_price', existing_type=sa.Integer(), nullable=False, server_default='0')

def downgrade():
    op.drop_column('collection_item', 'current_price')