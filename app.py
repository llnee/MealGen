# UI SERVICE

from flask import Flask, render_template, request, json
import os, sys
import psycopg2

script_dir = os.path.dirname( 'add_item.py' )
sys.path.append( script_dir )
from search import add_item_to_db, get_item_info, get_formatted_response
from connect_db import init_db


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/logged_in', methods=['GET', 'POST'])
def logged_in():
    return render_template('logged_in.html', form_data=request.form)


@app.route('/results', methods=['GET', 'POST'])
def search():
    item = request.form['search']
    photo, macros = get_formatted_response(get_item_info(item))  # first_food['photo'], str(nutrition_info)
    add_item_to_db(item)

    return render_template('results.html', item=item, photo=photo, macros=macros)


if __name__ == "__main__":
    init_db() # create new db at startup
    app.run()
