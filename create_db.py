from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
water_fufu = MenuItem(name="water fufu",
                      description="Water fufu and Eru made with kanda directly"
                                  " from South West Region", course="Entree", price= "500 XAF", restaurant = myFirstRestaurant)

session.add(water_fufu)
session.commit()
session.query(MenuItem).all()
