from app import app
from models import db, User

db.drop_all()
db.create_all()

User.register(
    first_name='test',
    last_name='test',
    email='test@test.com',
    password='test',
    cash=0,
)

User.register(
    first_name='test2',
    last_name='test2',
    email='test2@test2.com',
    password='test2',
    cash=0,
)

db.session.commit()
