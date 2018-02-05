from flask import Flask,jsonify,g,session\
 ,Blueprint,render_template,request,url_for\
 , redirect, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from resto.models import Restaurant, Base ,MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Define the blueprint: 'menuItem'
menuItem = Blueprint('menuItem', __name__,url_prefix='/menuItem')

@menuItem.route('/<int:restaurant_id>/',methods=['GET','POST'])
def items(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	menu_items = session.query(MenuItem).filter_by(restaurant = restaurant).all()
	return render_template('menuItem/all.html', items = menu_items, restaurant = restaurant, restaurant_id=restaurant_id)


@menuItem.route('/<int:restaurant_id>/new',methods=['GET','POST'])
def new(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST' :
		name = request.form['name'] 
		description = request.form['description']
		price = request.form['price']
		course = request.form['course']
		item = MenuItem(name=name,price=price, course=course, description=description, restaurant=restaurant)
		session.add(item)
		session.commit()
		return redirect(url_for('menuItem.items' , restaurant_id=restaurant_id))
	else:
		##### render Add page if request method is GET ####
		return render_template('menuItem/new.html', restaurant_id=restaurant_id, restaurant=restaurant)


@menuItem.route('/<int:restaurant_id>/<int:item_id>/edit',methods=['GET','POST'])
def edit(restaurant_id, item_id):
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
		return redirect(url_for('menuItem.items' , restaurant_id=restaurant_id))
    else:
		#render Edit page if request method is GET
		return render_template('menuItem/edit.html', restaurant = resto, item_id = item_id, item=item)


@menuItem.route('/<int:restaurant_id>/<int:item_id>/delete',methods=['GET','POST'])
def delete(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit
        return redirect(url_for('menuItem.items', restaurant_id=restaurant_id))
    else:
        #render delete Item page if request method is GET
        return render_template('menuItem/delete.html', item=item, restaurant_id=restaurant_id, item_id=item_id)

