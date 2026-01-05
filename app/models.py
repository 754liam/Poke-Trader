# Database models for users, cards, collections, and trades using SQLAlchemy
# Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt

from app import db, login_manager, bcrypt
from flask_login import UserMixin
import enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    balance = db.Column(db.Integer, default=1000, nullable=False)

    collection = db.relationship('CollectionItem', back_populates='owner', lazy=True)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_card_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    set_name = db.Column(db.String(100))
    image_url_small = db.Column(db.String(255))
    image_url_large = db.Column(db.String(255))
    price = db.Column(db.Integer, default=100, nullable=False)
    last_price_update = db.Column(db.Date, nullable=True)

    owners = db.relationship('CollectionItem', back_populates='card_info', lazy=True)

    def __repr__(self):
        return f'<Card {self.name} ({self.api_card_id})>'

class CollectionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)
    
    condition = db.Column(db.String(50), default='Near Mint')
    is_for_trade = db.Column(db.Boolean, default=True, nullable=False)
    purchase_price = db.Column(db.Integer, nullable=False, default=0)
    current_price = db.Column(db.Integer, nullable=False, default=0)

    owner = db.relationship('User', back_populates='collection')
    card_info = db.relationship('Card', back_populates='owners')

    def __repr__(self):
        return f'<CollectionItem {self.card_info.name} owned by {self.owner.username}>'

class TradeStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'

class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    proposer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    status = db.Column(db.Enum(TradeStatus), default=TradeStatus.PENDING, nullable=False)
    message = db.Column(db.Text, nullable=True)
    proposer_currency = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    proposer = db.relationship('User', foreign_keys=[proposer_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    offered_cards = db.relationship('OfferedCard', back_populates='trade', lazy=True, foreign_keys='OfferedCard.trade_id')
    requested_cards = db.relationship('RequestedCard', back_populates='trade', lazy=True)

class OfferedCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trade_id = db.Column(db.Integer, db.ForeignKey('trade.id'), nullable=False)
    collection_item_id = db.Column(db.Integer, db.ForeignKey('collection_item.id'), nullable=False)
    offering_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    trade = db.relationship('Trade', back_populates='offered_cards', foreign_keys=[trade_id])
    collection_item = db.relationship('CollectionItem')
    offering_user = db.relationship('User')

class RequestedCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trade_id = db.Column(db.Integer, db.ForeignKey('trade.id'), nullable=False)
    collection_item_id = db.Column(db.Integer, db.ForeignKey('collection_item.id'), nullable=False)
    requesting_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    trade = db.relationship('Trade', back_populates='requested_cards', foreign_keys=[trade_id])
    collection_item = db.relationship('CollectionItem')
    requesting_user = db.relationship('User')
