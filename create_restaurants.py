from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
yamo = Restaurant(name="TCHO TCHO ET YAMO")

session.add(yamo)
session.commit()


# Menu for UrbanBurger
restaurant1 = Restaurant(name="Urban Burger")
session.add(restaurant1)
session.commit()
# Menu for UrbanBurger
restaurant2 = Restaurant(name="King Burger")
session.add(restaurant2)
session.commit()
# Menu for UrbanBurger
restaurant3 = Restaurant(name="Mami Eru")
session.add(restaurant3)
session.commit()
# Menu for UrbanBurger
restaurant4 = Restaurant(name="Maguida")
session.add(restaurant4)
session.commit()
# Menu for UrbanBurger
restaurant5 = Restaurant(name="Senegalais")
session.add(restaurant5)
session.commit()
print('Operation Successfull')