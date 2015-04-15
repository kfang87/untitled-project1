# -*- coding: utf-8 -*-

import logging
import ntpath
from py2neo import Graph, Relationship
import procutils
import os
import sys
import ConfigParser
from os import listdir, path
import SourceNameMeaning

config = ConfigParser.ConfigParser()
config.read('config.ini')

create_names = False
create_descriptors = False
create_traits = False
create_person_name = False
create_descriptor_trait = False
create_person_descriptor = False
create_year = True
create_name_year = True
hydrate_name = True

# Graph functions

def getGraph():
    return Graph()

def ConfigureGraph(graph):
    if (graph.schema.get_uniqueness_constraints("Person").__len__() == 0):
        graph.schema.create_uniqueness_constraint("Person", "identifier")
    if (graph.schema.get_uniqueness_constraints("Descriptor").__len__() == 0):
        graph.schema.create_uniqueness_constraint("Descriptor", "descriptor_meaning_identifier")
    if (graph.schema.get_uniqueness_constraints("Characteristic").__len__() == 0):
        graph.schema.create_uniqueness_constraint("Characteristic", "word")
    if (graph.schema.get_uniqueness_constraints("Name").__len__() == 0):
        graph.schema.create_uniqueness_constraint("Name", "base_name")
    logging.info("Graph successfully configured with appropriate indexes")

# Node functions

def CreatePerson(graph, identifier, fullname, source_text):
    try:
        person = graph.merge_one("Person","identifier",identifier)
        person.properties["full_name"] = fullname
        person.properties["source"] = source_text
        person.push()
        logging.info("Person node created successfully for %s.",identifier)
    except:
        logging.warning("Problem with creating person %s",identifier)
    return person

def CreateDescriptor(graph, word):
    try:
        pos = "JJ"
        mlbl = "1"
        desciptor_meaning_identifier =  word.lower() + "-" + pos + "-" + mlbl
        descriptor = graph.merge_one("Descriptor", "descriptor_meaning_identifier", desciptor_meaning_identifier)
        descriptor["word"] = word.lower()
        descriptor["pos"] = pos
        descriptor["mlbl"] = mlbl
        descriptor.push()
        logging.info("Descriptor node created successfully for %ss.",desciptor_meaning_identifier)
    except:
        logging.warning("Problem with creating descriptor %s", word)
    return descriptor

def CreateCharacterTrait(graph, word):
    try:
        trait = graph.merge_one("Trait", "word", word.lower())
        trait.push()
        logging.info("Trait node created successfully for %ss.",word)
    except:
        logging.warning("Problem with creating trait %s",word)
    return trait

def CreateName(graph, firstname):
    try:
        name_node = graph.merge_one("Name","base_name",firstname)
        name_node.push()
        logging.info("Name node created successfully for %s.",firstname)
    except:
        logging.warning("Problem with creating name for %s",firstname)
    return name_node

def CreateYear(graph, year):
    try:
        year_node = graph.merge_one("Year","year",year)
        year_node.push()
        logging.info("Year node created successfully for %s", year)
    except:
        logging.warning("Problem with creating year for %s", year)
    return year_node

def HydrateName(graph,base_name, name_dict):
    try:
        name_node = graph.find_one("Name","base_name",base_name)
        if name_node:
            name_node.properties["origin"] = name_dict["origin"]
            name_node.properties["meaning"] = name_dict["meaning"]
            name_node.properties["gender"] = name_dict["gender"]
            name_node.push()
            logging.info("Hydrated name %s", base_name)
    except Exception as e:
        logging.warning("Problem with hydrating name %s with dictionary values %s", base_name, name_dict )

def RelateNameYear(graph, base_name, year, popularity_count):
    try:
        year_node = graph.find_one("Year","year", year)
        name_node = graph.find_one("Name","base_name",base_name)

        if not name_node:
            name_node = CreateName(graph, base_name)
        if not year_node:
            year_node = CreateYear(graph, year)
        r = Relationship(name_node, "GIVEN_IN", year_node, count=popularity_count)
        graph.create_unique(r)
        r.push()
        logging.info("Relationship GIVEN_IN created between %s and %s", name_node, year)
    except Exception as e:
        logging.warning("Problem with creating relationship between %s and %s: %s",base_name, year, e.message)
# Relationship functions

def RelatePersonHasName(graph, person_identifier, base_name):
    try:
        person = graph.find_one("Person", "identifier", person_identifier)
        name = graph.find_one("Name", "base_name",base_name)
        r = Relationship(person, "HAS_NAME", name)
        graph.create_unique(r)
        r.push()
        logging.info("Relationship HAS_NAME created between %s and %s",person_identifier, base_name)
    except:
        logging.warning("Problem with creating relationship between %s and %s",person_identifier, base_name)

def RelatePersonDescribedbyDescriptor(graph, person_identifier, descriptor_word_identifier, confidence_pct):
    try:
        person = graph.find_one("Person", "identifier", person_identifier)
        descriptor = graph.find_one("Descriptor", "descriptor_meaning_identifier", descriptor_word_identifier)
        r = Relationship(person, "DESCRIBED_BY", descriptor, confidence=confidence_pct)
        graph.create_unique(r)
        r.push()
        logging.info("Relationship DESCRIBED_BY created between %s and %s",person_identifier, descriptor_word_identifier)
    except:
        logging.warning("Problem with creating relationship between %s and %s",person_identifier, descriptor_word_identifier)

def RelateDescriptorSimilartytoTrait(graph, descriptor_word, trait_word, similarity_pct):
    descriptor_word_identifier = descriptor_word.lower() + "-JJ-1"
    try:
        descriptor = graph.find_one("Descriptor", "descriptor_meaning_identifier", descriptor_word_identifier)
        trait = graph.find_one("Trait","word", trait_word.lower())
        r = Relationship(descriptor, "IS_SIMILAR_TO", trait, similarity=similarity_pct )
        graph.create_unique(r)
        r.push()
        logging.info("Relationship IS_SIMILAR_TO created between %s and %s",descriptor_word_identifier, trait_word)
    except:
        logging.warning("Problem with creating relationship between %s and %s",descriptor_word_identifier, trait_word)

def MergePersonNodes(source_person_identifier, target_person_identifier, new_person_fullname, new_person_source_text):
    # if t and n are the same, or if n doesn't exist, update everything form s to t, delete s
    # if n exists and is not the same as t, fail
    graph = Graph()

    s_person = graph.find_one("Person","identifier",source_person_identifier)
    t_person = graph.find_one("Person","identifier",target_person_identifier)

    if (s_person):
        # if Target doesn't exist, create it
        if (not t_person):
            t_person = CreatePerson(graph, target_person_identifier, new_person_fullname, new_person_source_text)
        r_list = graph.match(start_node=s_person,bidirectional=True)
        if (r_list):
            for r in r_list:
                new_r = Relationship(t_person, r.type, r.end_node)
                new_r.properties = r.properties
                graph.create_unique(new_r)
                new_r.push()
        t_person.properties["full_name"] = new_person_fullname
        t_person.properties["source"] = new_person_source_text
        t_person.push()
        RemoveNode(graph,s_person)
    if (not s_person):
        logging.warning("Could not find required nodes using source person_identifier = %s", source_person_identifier)
        return

def RemoveNode(graph,node):
    if (node):
        try:
            for r in graph.match(start_node=node,bidirectional=True):
                graph.delete(r)
            node.delete()
            graph.push()
            logging.info("Successfully deleted relationships and node for Node: %s",node)
        except:
            logging.warning("Could not delete node %s with error %s", node, sys.exc_info())
    else:
        logging.warning("Could not delete node as it did not exist.")

def RemovePerson(person_identifier):
    graph = getGraph()
    person_node = graph.find_one("Person", "identifier", person_identifier)
    RemoveNode(graph,person_node)

def update_database():
    documents = procutils.get_documents()
    graph = getGraph()

    # Get all words from file
    vocabulary =  procutils.load_vocabulary()
    docterm_matrix, vocabulary_dict = procutils.create_doc_term_importance(documents, vocabulary)

    # BUILD THE GRAPH

    if (create_names):
        for doc in documents:
            CreateName(graph, procutils.get_name_from_docname(doc))

    if (create_descriptors):
        for word in vocabulary_dict:
            CreateDescriptor(graph,word)
    if (create_traits):
        with open(config.get('Data','TRAIT_FILEPATH')) as f:
            characteristics_array = f.read().splitlines()
        for char in characteristics_array:
            CreateCharacterTrait(graph,char)
    if (create_year):
        dir = config.get('Data','SSA_FILEPATH')
        for file in listdir(unicode(dir,'utf-8')):
            year = path.splitext(ntpath.basename(file))[0].replace("yob","")
            CreateYear(graph, year)
    if (create_name_year):
        dir = config.get('Data','SSA_FILEPATH')
        for file in listdir(unicode(dir,'utf-8')):
            year = path.splitext(ntpath.basename(file))[0].replace("yob","")
            with open(path.join(dir,file)) as f:
                line_list = f.read().splitlines()
                for line in line_list:
                    entry = line.split(',')
                    name = entry[0]
                    count = int(entry[2])
                    if count > 500:
                        RelateNameYear(graph,name,year,count)
    if (create_person_name):
        for doc in documents:
            RelatePersonHasName(graph, ntpath.basename(doc).replace(".txt",""),  procutils.get_name_from_docname(doc))
    if (create_descriptor_trait):
        with open(config.get('Data','TRAIT_FILEPATH')) as f:
            characteristics_array = f.read().splitlines()
        for char in characteristics_array:
            for word in vocabulary_dict:
                result = procutils.calculate_word_similarity_swoogle(word, char)
                if (result > 0.30):
                    RelateDescriptorSimilartytoTrait(graph,word, char, result)

    if (create_person_descriptor):
        for i,j,v in zip(docterm_matrix.row, docterm_matrix.col, docterm_matrix.data):
            person_identifier = ntpath.basename(documents[i]).replace(".txt","")
            word = str(vocabulary_dict[j]).encode('utf-8')
            affinity = v
            if (affinity > 0.01):
                affinity = str(affinity)
                word_identifier = word + "-JJ-1"
                RelatePersonDescribedbyDescriptor(graph,person_identifier,word_identifier,affinity)

    if (hydrate_name):
        name_list = graph.find("Name")
        for name_node in name_list:
            base_name = name_node.properties["base_name"]
            name_dict = SourceNameMeaning.retrieve_name_meaning(base_name)
            HydrateName(graph,base_name, name_dict)
def create_person_document(graph, person_name, context, source_text):

    DOCUMENT_FILEPATH = config.get('Sourcing','DOCUMENT_FILEPATH')
    entity_identifier = procutils.create_entity_identifier(person_name,source_text)
    filename = entity_identifier + '.txt'
    filepath = os.path.join(DOCUMENT_FILEPATH, filename)

    try:
        if (os.path.isfile(filepath) and os.path.getsize(filepath) > 0):
            logging.info('File already exists at %s, skipping file creation', filepath)
        else:
            with open(filepath,'w') as f:
                f.write(context)
            logging.info('Creating context file %s for entity %s', filepath, person_name)
            #add to database
        CreatePerson(graph,entity_identifier, person_name,source_text)
    except:
        logging.error('Could not complete creating file for filepath %s, %s',filename,sys.exc_info()[0])

    return filepath