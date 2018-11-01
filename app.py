from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from resto.models import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

#########  home page lists all Restaurants #########


@app.route('/')
@app.route('/restaurants')
def restaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants=restaurants)


###########  Add a new Restaurant ##################


@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		if request.form['name']:
			newResto = Restaurant(name=request.form['name'])
			session.add(newResto)
			session.commit()
			flash("New Restaurant Created")
			return redirect(url_for('restaurants'))
	else:
		#render New Restaurant page if request method is GET
		return render_template('newRestaurant.html')


##########  Edit Existing Restaurant ##############


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	old_resto = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			new_resto = request.form['name']
			old_resto.name = new_resto
			session.add(old_resto)
			session.commit()
			flash("Updated to %s",  new_resto)
			return redirect(url_for('restaurants'))
	else:
		#render Edit page if request method is GET
		return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=old_resto)


##########Delete Restaurant ####################

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	resto_to_delete = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(resto_to_delete)
		session.commit()
		flash("Was Deleted Successfuly")
		return redirect(url_for('restaurants'))
	else:
		#render Delete page if request method is GET
		return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=resto_to_delete)


################################ JSON RESPONSE  #################################################


#lists all Restaurants
@app.route('/restaurants/json')
def restaurantsJSON():
	restaurants = session.query(Restaurant).all()
	return jsonify(Restaurant=[i.serialize for i in restaurants])


#List all menu Items of a given restaurant in JSON
@app.route('/restaurants/<int:restaurant_id>/menuItems/json')
def menuItemsJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	menu_items = session.query(MenuItem).filter_by(restaurant=restaurant).all()
	return jsonify(MenuItem=[i.serialize for i in menu_items])


##############################Json Response End ###################################################


######################################## Menu Item CRUD Operations ################################################


############## Add a new menu Item #######################


@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newItem(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		name = request.form['name']
		description = request.form['description']
		price = request.form['price']
		course = request.form['course']
		item = MenuItem(name=name, price=price, course=course,
		                description=description, restaurant=restaurant)
		session.add(item)
		session.commit()
		return redirect(url_for('menuItems', restaurant_id=restaurant_id))
	else:
		##### render Add page if request method is GET ####

		return render_template('addMenuItem.html', restaurant_id=restaurant_id, restaurant=restaurant)


##### List all menu Items of a given restaurant ####

@app.route('/restaurants/<int:restaurant_id>/menuItems/')
def menuItems(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	menu_items = session.query(MenuItem).filter_by(restaurant=restaurant).all()
	return render_template('menuItems.html', items=menu_items, restaurant=restaurant, restaurant_id=restaurant_id)


####  Edit MenuItem #########

@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/editItem', methods=['GET', 'POST'])
def editItem(restaurant_id, item_id):
	resto = session.query(Restaurant).filter_by(id=restaurant_id).one()
	item = session.query(MenuItem).filter_by(id=item_id).one()
	if request.method == 'POST':
		name = request.form['name']
		description = request.form['description']
		price = request.form['price']
		item.name = name
		item.description = description
		item.price = price
		session.add(item)
		session.commit()
		return redirect(url_for('menuItems', restaurant_id=restaurant_id))
	else:
		#render Edit page if request method is GET
		return render_template('editItem.html', restaurant=resto, item_id=item_id, item=item)

#Delete Restaurant Item


@app.route('/restaurants/<int:restaurant_id>/<int:item_id>/deleteItem', methods=['GET', 'POST'])
def deleteItem(restaurant_id, item_id):
	item = session.query(MenuItem).filter_by(id=item_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit
		return redirect(url_for('menuItems', restaurant_id=restaurant_id))
	else:
		#render delete Item page if request method is GET
		return render_template('deleteMenuItem.html', item=item, restaurant_id=restaurant_id, item_id=item_id)


app.secret_key = 'super_secret_key'
if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
