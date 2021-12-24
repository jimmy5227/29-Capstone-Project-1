from app import app
from models import db, User

db.drop_all()
db.create_all()

u1 = User(
    first_name='test',
    last_name='test',
    email='test@test.com',
    password='test',
)

u2 = User(
    first_name='test2',
    last_name='test2',
    email='test2@test2.com',
    password='test2',
)

db.session.add_all([u1, u2])
db.session.commit()
