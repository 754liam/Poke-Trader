# Administrative script to delete all users and their data from the database
# Flask, Flask-SQLAlchemy

from app import create_app, db
from app.models import User, CollectionItem, Trade, OfferedCard, RequestedCard
app = create_app()
with app.app_context():
    print('⚠️  WARNING: This will delete ALL users and their data!')
    response = input("Type 'DELETE ALL' to confirm: ")
    if response == 'DELETE ALL':
        try:
            print('Deleting trade cards...')
            OfferedCard.query.delete()
            RequestedCard.query.delete()
            print('Deleting trades...')
            Trade.query.delete()
            print('Deleting collection items...')
            CollectionItem.query.delete()
            print('Deleting users...')
            user_count = User.query.count()
            User.query.delete()
            db.session.commit()
            print(f'✅ Successfully deleted {user_count} users and all related data!')
        except Exception as e:
            db.session.rollback()
            print(f'❌ Error: {e}')
    else:
        print('❌ Cancelled. No users were deleted.')