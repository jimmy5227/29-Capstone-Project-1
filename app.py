import os
# import pdb
import yfinance as yf

from flask import Flask, render_template, redirect, session, g, flash, request, jsonify, Response
from forms import UserAddForm, UserSignInForm
from models import db, connect_db, User, Stock
from sqlalchemy.exc import IntegrityError

import numpy as np
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

@app.route('/')
def index():
    if g.user:
        firstname = g.user.first_name
        return render_template('home.html', first_name=firstname)
    else:
        return render_template('home-anon.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user:
        firstname = g.user.first_name
        return render_template('home.html', first_name=firstname)

    else:
        form = UserSignInForm()
        if form.validate_on_submit():
            user = User.authenticate(form.email.data, form.password.data)
            if user:
                session[CURR_USER_KEY] = user.id
                g.user = user.id
                return redirect('/')
            else:
                flash('Incorerct username or password')
        return render_template('/users/login.html', form=form)

@app.route('/logout') # Best practice to have this be a POST
def logout():
    if CURR_USER_KEY in session:
        del g.user
        del session[CURR_USER_KEY]

    return redirect('/')

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

@app.route('/cash', methods=['GET', 'POST'])
def cash_page():
    if g.user:
        cash = g.user.cash
        return render_template('users/cash.html', cash=cash)
    else:
        redirect('/')

@app.route('/stock/<symbol>')
def stock_symbol(symbol):
    if g.user:
        stock = Stock.query.get_or_404(symbol)

        res = yf.Ticker(symbol)
        todays_data = res.history(period='1d')
        current_price = round(todays_data['Close'][0], 2)

        return render_template('stocks/symbol.html', stock=stock, price=current_price)
    else:
        return redirect('/')

@app.route('/stock/<symbol>/<endpoint>')
def fetch_endpoint(symbol, endpoint):
    if endpoint == 'currentPrice':
        res = yf.Ticker(symbol)
        todays_data = res.history(period='1d')
        current_price = round(todays_data['Close'][0], 2)
        return (jsonify(current_price))
    
    elif endpoint == 'getStock':
        stockRes = yf.Ticker(symbol)

        stockHistory = stockRes.history(period=request.args.get('period'), interval=request.args.get('interval'))
        # stockHistory = stockRes.history(period='5d', interval='5m')
        stockHistory = stockHistory.reset_index()
        stockHistory.columns = ['Date-Time']+list(stockHistory.columns[1:])
        max = (stockHistory['Open'].max())
        min = (stockHistory['Open'].min())
        range = max - min
        margin = range * 0.05
        max = max + margin
        min = min - margin
        fig = px.area(stockHistory, x='Date-Time', y="Open",
        hover_data=("Open","Close","Volume"), 
        range_y=(min,max), template="seaborn" )

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON
    
    elif endpoint == 'getInfo':
        request.args.get('data')
        stockRes = yf.Ticker(symbol)
        return json.dumps(stockRes.info)

    else:
        return 'Bad enpoint?', 400