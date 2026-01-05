# Initial database schema creation with users, cards, and collections
# Alembic, SQLAlchemy

from alembic import op
import sqlalchemy as sa
revision = '86c551ed8e16'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('card', sa.Column('id', sa.Integer(), nullable=False), sa.Column('api_card_id', sa.String(length=100), nullable=False), sa.Column('name', sa.String(length=100), nullable=False), sa.Column('set_name', sa.String(length=100), nullable=True), sa.Column('image_url_small', sa.String(length=255), nullable=True), sa.Column('image_url_large', sa.String(length=255), nullable=True), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('api_card_id'))
    op.create_table('user', sa.Column('id', sa.Integer(), nullable=False), sa.Column('username', sa.String(length=80), nullable=False), sa.Column('email', sa.String(length=120), nullable=False), sa.Column('password_hash', sa.String(length=128), nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'), sa.UniqueConstraint('username'))
    op.create_table('collection_item', sa.Column('id', sa.Integer(), nullable=False), sa.Column('user_id', sa.Integer(), nullable=False), sa.Column('card_id', sa.Integer(), nullable=False), sa.Column('condition', sa.String(length=50), nullable=True), sa.Column('is_for_trade', sa.Boolean(), nullable=False), sa.ForeignKeyConstraint(['card_id'], ['card.id']), sa.ForeignKeyConstraint(['user_id'], ['user.id']), sa.PrimaryKeyConstraint('id'))
    op.create_table('trade', sa.Column('id', sa.Integer(), nullable=False), sa.Column('proposer_id', sa.Integer(), nullable=False), sa.Column('receiver_id', sa.Integer(), nullable=False), sa.Column('status', sa.Enum('PENDING', 'ACCEPTED', 'REJECTED', 'CANCELLED', name='tradestatus'), nullable=False), sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True), sa.ForeignKeyConstraint(['proposer_id'], ['user.id']), sa.ForeignKeyConstraint(['receiver_id'], ['user.id']), sa.PrimaryKeyConstraint('id'))
    op.create_table('offered_card', sa.Column('id', sa.Integer(), nullable=False), sa.Column('trade_id', sa.Integer(), nullable=False), sa.Column('collection_item_id', sa.Integer(), nullable=False), sa.Column('offering_user_id', sa.Integer(), nullable=False), sa.ForeignKeyConstraint(['collection_item_id'], ['collection_item.id']), sa.ForeignKeyConstraint(['offering_user_id'], ['user.id']), sa.ForeignKeyConstraint(['trade_id'], ['trade.id']), sa.PrimaryKeyConstraint('id'))

def downgrade():
    op.drop_table('offered_card')
    op.drop_table('trade')
    op.drop_table('collection_item')
    op.drop_table('user')
    op.drop_table('card')