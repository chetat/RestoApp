from flask import Flask, g, session, Blueprint, jsonify, render_template, request, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from resto.models import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

restaurant = Blueprint('restaurant', __name__, url_prefix='/')
####### configuration #####


@restaurant.route('/')
def restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants/all.html', restaurants=restaurants)


@restaurant.route('new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if request.form['name']:
			newResto = Restaurant(name=request.form['name'])
			session.add(newResto)
			session.commit()
			flash("New Restaurant Created")
			return redirect(url_for('restaurant.restaurants'))
    else:
		#render New Restaurant page if request method is GET
		return render_template('restaurants/new.html')

##########  Edit Existing Restaurant ##############


@restaurant.route('<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit(restaurant_id):
    old_resto = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            new_resto = request.form['name']
            old_resto.name = new_resto
            session.add(old_resto)
            session.commit()
            flash("Updated to %s",  new_resto)
            return redirect(url_for('restaurant.restaurants'))
    else:
        #render Edit page if request method is GET
        return render_template('restaurants/edit.html', restaurant_id=restaurant_id, restaurant=old_resto)


##########Delete Restaurant ####################
@restaurant.route('<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete(restaurant_id):
    resto_to_delete = session.query(
    	Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
		session.delete(resto_to_delete)
		session.commit()
		flash("Was Deleted Successfuly")
		return redirect(url_for('restaurant.restaurants'))
    else:
		#render Delete page if request method is GET
		return render_template('restaurants/delete.html', restaurant_id=restaurant_id, restaurant=resto_to_delete)
