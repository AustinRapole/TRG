import sys 
#sys.path.append("../")
#from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template
from __init__ import create_app

#sys.path.append("../")

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
  title = 'Toadally Real Graphs'
  data = {'title': 'Welcome to our home page', 'options': ['Bibliography', 'Formulas', 'Graphs']}
  return render_template('home.html', title=title, data=data)

@app.route('/input')
def input():
  return render_template('input.html')
@app.route('/bib')
def bib():
  return render_template('bib.html')

if __name__ == '__main__':
    app.run(debug=True)

