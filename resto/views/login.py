# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session as login_session, redirect, url_for
import random
import string
#oauth  Imports
#IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

#Import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# Import password / encryption helper tools
#from werkzeug.security import check_password_hash, generate_password_hash

# Import module forms
#from resto.auth.forms import LoginForm

# Import module models (i.e. User)
#from resto.auth.models import Users

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']
APPLICATION_NAME = "Boberesto"

#initialise DB Engine
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Define the blueprint: 'login'
login = Blueprint('login', __name__, url_prefix='/login')


@login.route('/')
def showlogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))

    login_session['state'] = state
    return render_template("auth/login.html", STATE=state)


@login.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        pass
