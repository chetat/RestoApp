from flask import Flask,jsonify,Blueprint, render_template,request,url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from resto.models import Restaurant, Base ,MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

json = Blueprint('json', __name__,url_prefix='/api')

app = Flask(__name__)



################################ JSON RESPONSE  #################################################


#lists all Restaurants
@json.route('/restaurants/json')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurant=[i.serialize for i in restaurants])

#List all menu Items of a given restaurant in JSON
@json.route('/restaurants/<string:restaurant_name>/items/json')
def ItemsJSON(restaurant_name):
	restaurant = session.query(Restaurant).filter_by(name=restaurant_name).one()
	menu_items = session.query(MenuItem).filter_by(restaurant = restaurant).all()
	return jsonify(MenuItem=[i.serialize for i in menu_items])

#List all menu Items of a given restaurant in JSON
@json.route('/restaurants/items/json')
def menuItemsJSON():
	menu_items = session.query(MenuItem).all()
	return jsonify(MenuItem=[i.serialize for i in menu_items])



##############################Json Response End ###################################################

