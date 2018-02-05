# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
#Import sqlalchemy 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash

# Import module forms
from resto.auth.forms import LoginForm

# Import module models (i.e. User)
from resto.auth.models import Users

#initialise DB Engine
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Define the blueprint: 'login'
login = Blueprint('login', __name__,url_prefix='/auth')

@login.route('/', methods=['GET','POST'])
def index():
    return render_template("auth/login.html")