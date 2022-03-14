from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    # location = db.Column(
    #     db.Text,
    # )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.first_name} {self.last_name} AS: {self.username}, {self.email}>"

    @classmethod
    def register(cls, first_name, last_name, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Stock(db.Model):

    __tablename__ = 'stocks'

    symbol = db.Column(
        db.String,
        primary_key=True,
        nullable=False
    )

    name = db.Column(
        db.String,
        nullable=False
    )

    exchange = db.Column(
        db.String,
        nullable=False
    )

    country_name = db.Column(
        db.String,
        nullable=False
    )

    sector = db.Column(
        db.String,
        nullable=False
    )

    industry = db.Column(
        db.String,
        nullable=False
    )

    about = db.Column(
        db.Text,
        nullable=False
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )