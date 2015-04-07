__author__ = 'Kayla'
from flask import Flask, redirect, url_for, request, render_template
from flask import  jsonify
from py2neo import Graph, Node

app = Flask(__name__)

@app.route('/', methods =['POST','GET'])
def index():
    if request.method == 'POST':
        if(request.form['name']):
            return redirect(url_for('display_name_results',base_name=request.form['name']))
        elif(request.form['trait']):
            return redirect(url_for('display_trait_results',trait_word=request.form['trait']))
    else:
        return render_template('index.html')

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
    person_dict = {}

    query = "MATCH (n:Name) -[r]- (p:Person) - [r2] - (d:Descriptor) -[r3]- (t:Trait {{word:'{}'}}) " \
            "return p.identifier as person_identifier, " \
            "p.full_name as person_full_name, " \
            "p.source as person_source, " \
            "sum( toFloat(r2.confidence) * toFloat(r3.similarity))as rating " \
            "ORDER BY rating DESC " \
            "LIMIT 50".format(trait_word.lower())

    records = graph.cypher.execute(query)

    for r in records:
        person_identifier = r["person_identifier"]
        person_full_name = r["person_full_name"]
        person_source = r["person_source"]
        rating = r["rating"]
        person_dict[person_identifier]  = {"full_name" : person_full_name,
                     "source" : person_source,
                     "rating" : rating}
    return jsonify(person_dict)

if __name__ == '__main__':
    app.run(debug=True)