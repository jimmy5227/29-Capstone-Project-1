from app import app
from models import db, User

db.drop_all()
db.create_all()

User.register(
    first_name='test',
    last_name='test',
    email='test@test.com',
    password='test',
)

User.register(
    first_name='test2',
    last_name='test2',
    email='test2@test2.com',
    password='test2',
)

db.session.commit()
