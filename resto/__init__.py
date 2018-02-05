from flask import Flask

from resto.views.login import login 
from resto.views.restaurant import restaurant 
from resto.views.menuItem import menuItem 
from resto.views.api import json 

app = Flask(__name__)

# Configurations
app.config.from_object('config')
 
app.register_blueprint(restaurant)
app.register_blueprint(login)
app.register_blueprint(menuItem)
app.register_blueprint(json)

