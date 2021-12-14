import os

from flask import Flask, render_template, redirect, session, g
from forms import UserAddForm
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///capstone'))
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "Capstone")

connect_db(app)

@app.route('/')
def index():
    # if g.user:
    # return render_template('home.html')
    # else:
    return render_template('home-anon.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = UserAddForm()

    if form.validate_on_submit():
        # try:
        user = User.register(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.commit()

        session[CURR_USER_KEY] = user.id

        # except IntegrityError:
        #     flash("Username already taken", 'danger')
        # return render_template('users/signup.html', form=form)

        # return redirect("/")
        return ('<h1>It worked</h1>')
    return render_template('users/register.html', form=form)