__author__ = 'Kayla'
from flask import Flask, redirect, url_for, request, render_template, session
from flask import  jsonify
import dbaccess
import logging, logging.config
import sys
from collections import deque

app = Flask(__name__)

@app.route('/', methods =['POST','GET'])
def index():
    try:
        if request.method == 'POST':
            if(request.form['base_name']):
                base_name=request.form['base_name']
                return redirect(url_for('display_name_results',base_name=base_name))
            elif(request.form['trait_word']):
                return redirect(url_for('display_trait_results',trait_word=request.form['trait_word']))
        else:
            traits = dbaccess.get_traits_list()
            return render_template('index.html',traits=traits)
    except:
        logger.error("PROBLEM: %s", sys.exc_info())
        return redirect(url_for('error'))
# For a name, return most popular traits via the people they are associated with

@app.route('/error')
def error():
    return render_template('error.html'), 404

@app.route('/about')
def about():
    return render_template('about.html')

#API
@app.route('/api/name/<base_name>', methods=['GET'])
def display_name_results(base_name):
    name_dict = {}
    name_dict["persons"] = dbaccess.get_person_dict_for_name(base_name)
    name_dict["attributes"] = dbaccess.get_attributes_dict_for_name(base_name)
    name_dict["popularity"] = dbaccess.get_popularity_dict_for_name(base_name)
    update_cookie_list(session,"searched_names",base_name)
    return jsonify(name_dict)

@app.route('/api/trait/<trait_word>')
def display_trait_results(trait_word):
    update_cookie_list(session,"searched_traits",trait_word)
    return jsonify(dbaccess.get_name_dict_for_trait(trait_word))

@app.route('/ui/trait/<trait_word>')
def show_trait_results(trait_word):
    results = display_trait_results(trait_word)

def update_cookie_list(session, cookie_key, new_value):
    list = []
    if cookie_key in session:
        list = deque(session[cookie_key].split(","))
        logging.info("here 1")
    list.append(new_value)
    while list.__len__() > 10:
        list.popleft()
    session[cookie_key] = ",".join(list)
    logging.info("here 2 %s", session[cookie_key])
    return session[cookie_key]

def get_cookie_list(session, cookie_key):
    return session[cookie_key].split(",")

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger('root')
    logger.info('Logging Started.')
    app.secret_key = 'test123'
    app.run(debug=True)