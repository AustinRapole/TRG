import sys 
sys.path.append("../")
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template
from __init__ import create_app

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)
def test(name=None):
  return render_template("template.html", name=name)
env = Environment(loader=FileSystemLoader('templates'))
#template = env.get_template('template.html')
output = template.render(create_app)
print(output)
