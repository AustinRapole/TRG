from flask import Flask, render_template
from end_points import *

def create_app():

   # intializing Flask
   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'jdvbonfewhf ewfwepuihfnv'

   #registers the two files that contain the Flask blueprints
   app.register_blueprint(end_points, url_prefix='/')

   #thing to connect html
   @app.route('/')
   def landing():
     return render_template('home.html')

   @app.route('/bib')
   def bibliography():
     return render_template('bib.html')

   @app.route('/input')
   def input():
     return render_template('input.html')

   return app
