# Add currency support to trade proposals
# Alembic, SQLAlchemy

from alembic import op
import sqlalchemy as sa
revision = 'add_trade_currency'
down_revision = 'add_currency_pricing'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('trade', sa.Column('proposer_currency', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('trade', 'proposer_currency')