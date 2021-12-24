import os

from flask import Flask, render_template, redirect, session, g
from forms import UserAddForm, UserSignInForm
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///WSB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "WSB")


connect_db(app)
db.create_all()

CURR_USER_KEY = "curr_user"

@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

@app.route('/')
def index():
    if g.user:
        return ('<h1>It worked</h1>')
    else:
        form = UserSignInForm()

        print('************************')
        print('Form loaded')
        print('************************')

        if form.validate_on_submit():
            user = User.authenticate(form.email.data, form.password.data)
            
            print('************************')
            print(user)
            print('************************')

            if user:
                session[CURR_USER_KEY] = user.id
                g.user = user.id
                return redirect('/')

        return render_template('home-anon.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = UserAddForm()

    if form.validate_on_submit():
        # try:
        user = User.register(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.commit()

        session[CURR_USER_KEY] = user.id
        g.user = user.id

        # except IntegrityError:
        #     flash("Username already taken", 'danger')
        # return render_template('users/signup.html', form=form)

        return redirect('/')
    return render_template('users/register.html', form=form)
