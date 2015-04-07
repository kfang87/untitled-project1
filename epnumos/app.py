__author__ = 'Kayla'
from flask import Flask, redirect, url_for, request, render_template
from flask import  jsonify
from py2neo import Graph, Node
import logging, logging.config
import sys

app = Flask(__name__)

@app.route('/', methods =['POST','GET'])
def index():
    try:
        if request.method == 'POST':
            if(request.form['base_name']):
                return redirect(url_for('display_name_results',base_name=request.form['base_name']))
            elif(request.form['trait_word']):
                return redirect(url_for('display_trait_results',trait_word=request.form['trait_word']))
        else:
            return render_template('index.html',traits=list_traits())
    except:
        logger.error("PROBLEM: %s", sys.exc_info())
# For a name, return most popular traits via the people they are associated with

@app.route('/epnomus/api/name/<base_name>', methods=['GET'])
def display_name_results(base_name):
    graph = Graph()
    person_dict = {}

    query = ("MATCH (n:Name {{base_name: '{0}'}}) -[r]- (p:Person) -[r2]-(d:Descriptor) -[r3]- (t:Trait) " \
            "RETURN p.identifier as person_identifier, " \
            "p.full_name as person_full_name, " \
            "p.source as person_source, " \
            "t.word as trait, " \
            "sum( toFloat(r2.confidence) * toFloat(r3.similarity))as rating " \
            "ORDER BY p.identifier,rating desc")\
            .format(base_name)
    records = graph.cypher.execute(query)

    for r in records:

        person_identifier = r["person_identifier"]
        person_full_name = r["person_full_name"]
        person_source = r["person_source"]
        trait = r["trait"]
        rating = r["rating"]


        person_value = {}

        # If person exists, retrieve and add to the trait
        if person_dict.has_key(person_identifier):
            person_value = person_dict[person_identifier]
            trait_dict = person_value["traits"]
            trait_dict[trait] = round(rating,2)
            person_value["traits"] = trait_dict
        else: #initialize personal and traits dictionary
            person_value["personal"] = {"full_name": person_full_name, "source" : person_source }
            person_value["traits"] = {trait: round(rating,2)}

        person_dict[person_identifier] = person_value

    return jsonify(person_dict)

@app.route('/epnomus/api/trait/<trait_word>')
def display_trait_results(trait_word):
    graph = Graph()
    name_dict = {}

    query = "MATCH (n:Name) -[r]- (p:Person) - [r2] - (d:Descriptor) -[r3]- (t:Trait {{word:'{}'}}) " \
            "WHERE length(n.base_name) > 0 " \
            "return n.base_name as base_name," \
            "p.identifier as person_identifier, " \
            "p.full_name as person_full_name, " \
            "p.source as person_source, " \
            "sum( toFloat(r2.confidence) * toFloat(r3.similarity))as rating " \
            "ORDER BY rating DESC " \
            "LIMIT 100".format(trait_word.lower())

    records = graph.cypher.execute(query)

    for r in records:
        person_identifier = r["person_identifier"]
        person_full_name = r["person_full_name"]
        person_source = r["person_source"]
        rating = r["rating"]
        basename = r["base_name"]
        person_dict = {}
        if name_dict.has_key(basename):
            person_dict = name_dict[basename]
        if not person_dict.has_key(person_identifier):
            person_dict[person_identifier]  = {"base_name": basename,
                         "full_name" : person_full_name,
                         "source" : person_source,
                         "rating" : round(rating,2)}
        name_dict[basename] = person_dict
    return jsonify(name_dict)

def list_traits():
    graph = Graph()
    trait_list = graph.find("Trait")
    return trait_list

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger('root')
    logger.info('Logging Started.')
    app.run(debug=True)