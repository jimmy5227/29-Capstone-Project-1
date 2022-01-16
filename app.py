import os
# import pdb
import yfinance as yf

from flask import Flask, render_template, redirect, session, g, flash, request
from forms import UserAddForm, UserSignInForm
from models import db, connect_db, User
from sqlalchemy.exc import IntegrityError

import pandas as pd
import json
import plotly
import plotly.express as px

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

# @app.route('/history')
# def history():
#     symbol = request.args.get('symbol', default="AAPL")
#     aapl = yf.Ticker(symbol)
#     period = request.args.get('period', default="1y")
#     interval = request.args.get('interval', default="1mo")        

@app.route('/', methods = ['GET', 'POST'])
def index():
    if g.user:
        # symbol = request.args.get('symbol', default="AAPL")
        # # aapl = yf.Ticker(symbol)
        # period = request.args.get('period', default="1y")
        # interval = request.args.get('interval', default="1mo")        
        # quote = yf.Ticker(symbol)   
        # hist = quote.history(period=period, interval=interval)
        # data = hist.to_json()
        # # return data

        # # return aapl.info
        return render_template('home.html')
    else:

        form = UserSignInForm()

        if form.validate_on_submit():
            
            user = User.authenticate(form.email.data, form.password.data)

            if user:
                session[CURR_USER_KEY] = user.id
                g.user = user.id
                return redirect('/')

        return render_template('home-anon.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.commit()

            session[CURR_USER_KEY] = user.id
            g.user = user.id

        except IntegrityError:
            flash("Email already taken", 'danger')
            return ('<h1>Email already taken</h1>')

        return redirect('/')
    return render_template('users/register.html', form=form)

@app.route('/callback/<endpoint>')
def cb(endpoint):   
    if endpoint == "getStock":
        return gm(request.args.get('data'),request.args.get('period'),request.args.get('interval'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        st = yf.Ticker(stock)
        return json.dumps(st.info)
    else:
        return "Bad endpoint", 400

# Return the JSON data for the Plotly graph
def gm(stock,period, interval):
    st = yf.Ticker(stock)
  
    # Create a line graph
    df = st.history(period=(period), interval=interval)
    df=df.reset_index()
    df.columns = ['Date-Time']+list(df.columns[1:])
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date-Time', y="Open",
        hover_data=("Open","Close","Volume"), 
        range_y=(min,max), template="seaborn" )

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON