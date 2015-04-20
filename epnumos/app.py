__author__ = 'Kayla'
import logging
import logging.config
import sys
from collections import OrderedDict
from flask import request

from flask import Flask, redirect, url_for, request, render_template, session
from flask import  jsonify

import dbaccess


app = Flask(__name__)

@app.route('/', methods =['POST','GET'])
def index():
    try:
        if request.method == 'POST':
            if(request.form['base_name']):
                base_name=request.form['base_name']
                return redirect(url_for('show_name_results',base_name=base_name))
            elif(request.form['trait_word']):
                return redirect(url_for('show_trait_results',trait_word=request.form['trait_word']))
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
    return jsonify({base_name : name_dict})

@app.route('/api/trait/<trait_word>')
def display_trait_results(trait_word):
    return jsonify(dbaccess.get_name_dict_for_trait(trait_word))

@app.route('/ui/trait/<trait_word>')
def show_trait_results(trait_word):
    update_cookie_list(session,"searched_traits",trait_word)
    name_dict = dbaccess.get_name_dict_for_trait(trait_word)
    return render_template('show_trait.html',res=name_dict,trait=trait_word)

@app.route('/ui/name/<base_name>')
def show_name_results(base_name):
    name_dict = {}
    name_dict["persons"] = OrderedDict(sorted(dbaccess.get_person_dict_for_name(base_name).items(), key=lambda p: p[0])) # dbaccess.get_person_dict_for_name(base_name)
    name_dict["attributes"] = dbaccess.get_attributes_dict_for_name(base_name)
    name_dict["popularity"] = dbaccess.get_popularity_dict_for_name(base_name)
    update_cookie_list(session,"searched_names",base_name)
    return render_template('show_name.html',res=name_dict, name=base_name.capitalize())

def get_trait_results(trait_word):
    return dbaccess.get_name_dict_for_trait(trait_word)

def update_cookie_list(session, cookie_key, new_value):
    list = []
    if cookie_key in session:
        list = session[cookie_key].split(",")
    if not list.__contains__(new_value):
        list.append(new_value)
    while list.__len__() > 10:
        del list[0]
    session[cookie_key] = ",".join(list)
    return session[cookie_key]

def get_cookie_list(session, cookie_key):
    return session[cookie_key].split(",")

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger('root')
    logger.info('Logging Started.')
    app.secret_key = 'test123'
    app.run(debug=True)