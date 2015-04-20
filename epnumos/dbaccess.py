__author__ = 'Kayla'
from py2neo import Graph
import HTMLParser
from collections import OrderedDict

graph = Graph()
h = HTMLParser.HTMLParser()
# Name queries

def get_person_dict_for_name( base_name):

    person_dict = {}

     # Fill in persons dictionary
    query = ("MATCH (n:Name {{base_name: '{0}'}}) -[r]- (p:Person) -[r2]-(d:Descriptor) -[r3]- (t:Trait) " \
            "RETURN p.identifier as person_identifier, " \
            "p.full_name as person_full_name, " \
            "p.source as person_source, " \
            "t.word as trait, " \
            "sum( toFloat(r2.confidence) * toFloat(r3.similarity))as rating " \
            "ORDER BY p.identifier,rating desc")\
            .format(base_name.lower())
    records =  graph.cypher.execute(query)
    for r in records:
        person_identifier = r["person_identifier"]
        person_full_name = h.unescape(r["person_full_name"])
        person_source = h.unescape(r["person_source"])
        trait = r["trait"]
        rating = r["rating"]

        person_value = {}

        # If person exists, retrieve and add to the trait
        if person_dict.has_key(person_identifier):
            person_value = person_dict[person_identifier]
            trait_dict = person_value["traits"]
            trait_dict[trait] = round(rating,2)
            person_value["traits"] = OrderedDict(sorted(trait_dict.items(),key=lambda trait : trait[1], reverse=True))
        else: #initialize personal and traits dictionary
            person_value["personal"] = {"full_name": person_full_name, "source" : person_source }
            person_value["traits"] = {trait: round(rating,2)}

        person_dict[person_identifier] = person_value

    return person_dict

def get_popularity_dict_for_name(base_name):
    popularity_dict = {}

    year_query = ("MATCH (n:Name {{base_name:'{0}'}}) -[r:GIVEN_IN] - (y:Year) " \
              "RETURN y.year as year, " \
              "r.count as count")\
                .format(base_name.lower())
    popularity_records = graph.cypher.execute(year_query)

    for r in popularity_records:
        popularity_dict[r["year"]] = r["count"]

    return popularity_dict

def get_attributes_dict_for_name(base_name):
    attributes_dict = {}
    name_node = graph.find_one("Name", "base_name", base_name)
    if name_node:
        attributes_dict["gender"] = name_node.properties["gender"]
        attributes_dict["origin"] = name_node.properties["origin"]
        attributes_dict["meaning"] = name_node.properties["meaning"]
    return attributes_dict

def get_name_dict_for_trait(trait_word):
    name_dict = {}
    query = "MATCH (n:Name) -[r]- (p:Person) - [r2] - (d:Descriptor) -[r3]- (t:Trait {{word:'{}'}}) " \
            "WHERE length(n.base_name) > 0 " \
            "return n.display_name as base_name," \
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
        person_full_name = h.unescape(r["person_full_name"])
        person_source = h.unescape(r["person_source"])
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
        name_dict[basename]["persons"] = OrderedDict(sorted(person_dict.items(),key=lambda person: person[1]["rating"],reverse=True))
        name_dict[basename]["origin"] = origin
        name_dict[basename]["gender"] = gender
        name_dict[basename]["meaning"] = meaning
        if not name_dict[basename].has_key("max_rating") or  rating > name_dict[basename]["max_rating"]:
            name_dict[basename]["max_rating"] = rating

    return {"names": OrderedDict(sorted(name_dict.items(),key=lambda name: (name[1]["max_rating"]),reverse=True))}

def get_traits_list():
    word_list = map(extract_trait_word,graph.find("Trait"))
    word_list.sort()
    return word_list

def extract_trait_word(trait_entry):
    return trait_entry.properties["word"]