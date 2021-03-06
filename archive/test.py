from py2neo import Graph
from flask import json

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
            trait_dict[trait] = rating
            person_value["traits"] = trait_dict
        else: #initialize personal and traits dictionary
            person_value["personal"] = {"full_name": person_full_name, "source" : person_source }
            person_value["traits"] = {trait: rating}

        person_dict[person_identifier] = person_value

    print person_dict

display_name_results("Jane")