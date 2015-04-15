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

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/epnomus/api/name/<base_name>', methods=['GET'])
def display_name_results(base_name):
    graph = Graph()
    person_dict = {}
    attributes_dict = {}
    name_dict = {}

    # Fill in persons dictionary
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

        name_dict["persons"] = person_dict

    # Fill in name's basic attributes
    name_node = graph.find_one("Name", "base_name", base_name)
    if name_node:

        attributes_dict["gender"] = name_node.properties["gender"]
        attributes_dict["origin"] = name_node.properties["origin"]
        attributes_dict["meaning"] = name_node.properties["meaning"]


    # Fill in name's popularity attribute
    year_query = ("MATCH (n:Name {{base_name:'{0}'}}) -[r:GIVEN_IN] - (y:Year) " \
                  "RETURN y.year as year, " \
                  "r.count as count")\
                    .format(base_name)
    popularity_records = graph.cypher.execute(year_query)
    year_dict = {}
    for r in popularity_records:
        year_dict[r["year"]] = r["count"]
    attributes_dict["popularity"] = year_dict

    # Attach attributes to main name entry
    name_dict["attributes"] = attributes_dict

    return jsonify(name_dict)

@app.route('/epnomus/api/trait/<trait_word>')
def display_trait_results(trait_word):
    graph = Graph()
    name_dict = {}

    query = "MATCH (n:Name) -[r]- (p:Person) - [r2] - (d:Descriptor) -[r3]- (t:Trait {{word:'{}'}}) " \
            "WHERE length(n.base_name) > 0 " \
            "return n.base_name as base_name," \
            "n.origin as origin," \
            "n.gender as gender," \
            "n.meaning as meaning," \
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
        origin = r["origin"]
        gender = r["gender"]
        meaning = r["meaning"]
        person_dict = {}
        if name_dict.has_key(basename):
            if name_dict[basename].has_key("persons"):
                person_dict = name_dict[basename]["persons"]
        else:
            name_dict[basename]  = {}

        if not person_dict.has_key(person_identifier):
            person_dict[person_identifier]  = {"full_name" : person_full_name,
                         "source" : person_source,
                         "rating" : round(rating,2)}
        name_dict[basename]["persons"] = person_dict
        name_dict[basename]["origin"] = origin
        name_dict[basename]["gender"] = gender
        name_dict[basename]["meaning"] = meaning
    return jsonify(name_dict)

def list_traits():
    graph = Graph()
    word_list = map(extract_trait_word,graph.find("Trait"))
    word_list.sort()
    return word_list

def extract_trait_word(trait_entry):
    return trait_entry.properties["word"]

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    logger = logging.getLogger('root')
    logger.info('Logging Started.')
    app.run(debug=True)