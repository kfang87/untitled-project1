# -*- coding: utf-8 -*-

import logging
import ConfigParser
from py2neo import Graph, Relationship
import untitledutils
import ntpath

create_names = False
create_descriptors = False
create_traits = False
create_person_name = False
create_descriptor_trait = False
create_person_descriptor = True

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
    logger.info("Graph successfully configured with appropriate indexes")

# Node functions

def CreatePerson(graph, identifier, fullname, source_text):
    try:
        person = graph.merge_one("Person","identifier",identifier)
        person.properties["full_name"] = fullname
        person.properties["source"] = source_text
        person.push()
        logger.info("Person node created successfully for %s.",identifier)
    except:
        logger.warning("Problem with creating person %s",identifier)
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
        logger.info("Descriptor node created successfully for %ss.",desciptor_meaning_identifier)
    except:
        logger.warning("Problem with creating descriptor %s", word)
    return descriptor

def CreateCharacterTrait(graph, word):
    try:
        trait = graph.merge_one("Trait", "word", word.lower())
        trait.push()
        logger.info("Trait node created successfully for %ss.",word)
    except:
        logger.warning("Problem with creating trait %s",word)
    return trait

def CreateName(graph, firstname):
    try:
        name = graph.merge_one("Name","base_name",firstname)
        name.push()
        logger.info("Name node created successfully for %ss.",firstname)
    except:
        logger.warning("Problem with creating name for %s",firstname)
    return firstname

# Relationship functions

def RelatePersonHasName(graph, person_identifier, base_name):
    try:
        person = graph.find_one("Person", "identifier", person_identifier)
        name = graph.find_one("Name", "base_name",base_name)
        r = Relationship(person, "HAS_NAME", name)
        graph.create_unique(r)
        r.push()
        logger.info("Relationship HAS_NAME created between %s and %s",person_identifier, base_name)
    except:
        logger.warning("Problem with creating relationship between %s and %s",person_identifier, base_name)

def RelatePersonDescribedbyDescriptor(graph, person_identifier, descriptor_word_identifier, confidence_pct):
    try:
        person = graph.find_one("Person", "identifier", person_identifier)
        descriptor = graph.find_one("Descriptor", "descriptor_meaning_identifier", descriptor_word_identifier)
        r = Relationship(person, "DESCRIBED_BY", descriptor, confidence=confidence_pct)
        graph.create_unique(r)
        r.push()
        logger.info("Relationship DESCRIBED_BY created between %s and %s",person_identifier, descriptor_word_identifier)
    except:
        logger.warning("Problem with creating relationship between %s and %s",person_identifier, descriptor_word_identifier)

def RelateDescriptorSimilartytoTrait(graph, descriptor_word_identifier, trait_word, similarity_pct):
    try:
        descriptor = graph.find_one("Descriptor", "descriptor_meaning_identifier", descriptor_word_identifier)
        trait = graph.find_one("Trait","word", trait_word.lower())
        r = Relationship(descriptor, "IS_SIMILAR_TO", trait, similarity=similarity_pct )
        graph.create_unique(r)
        r.push()
        logger.info("Relationship IS_SIMILAR_TO created between %s and %s",descriptor_word_identifier, trait_word)
    except:
        logger.warning("Problem with creating relationship between %s and %s",descriptor_word_identifier, trait_word)

def MergePeople(source_person_identifier, target_person_identifier, new_person_identifier, target_person_fullname, target_person_source_text):
    # add text from source to target, delete source file
    # rename file using new_person_identifier
    # update the node attributes from source to target
    # delete source node
    print 'TODO'
    
def update_database():
    documents = untitledutils.get_documents()
    graph = getGraph()

    # Get all words from file
    vocabulary =  untitledutils.load_vocabulary()
    docterm_matrix, vocabulary_dict = untitledutils.create_doc_term_importance(documents, vocabulary)

    # BUILD THE GRAPH

    if (create_names):
        for doc in documents:
            CreateName(graph, untitledutils.get_name_from_docname(doc))

    if (create_descriptors):
        for word in vocabulary_dict.iterkeys():
            CreateDescriptor(graph,word)
    if (create_traits):
        characteristics_file = open('C:\code\untitled-project1\data\character_traits.txt')
        characteristics_file.readline()
        characteristics_array = characteristics_file.read().split('\n')
        characteristics_file.close()
        for char in characteristics_array:
            CreateCharacterTrait(graph,char)
    if (create_person_name):
        for doc in documents:
            RelatePersonHasName(graph, ntpath.basename(doc).replace(".txt",""),  untitledutils.get_name_from_docname(doc))

    if (create_descriptor_trait):
        for char in characteristics_array:
            for word in vocabulary_dict:
                result = untitledutils.calculate_word_similarity(word, char)
                if (result > 0.05):
                    RelateDescriptorSimilartytoTrait(graph,word + "-JJ-1", char, result)

    if (create_person_descriptor):
        for i,j,v in zip(docterm_matrix.row, docterm_matrix.col, docterm_matrix.data):
            person_identifier = ntpath.basename(documents[i]).replace(".txt","")
            word = str(vocabulary_dict[j]).encode('utf-8')
            affinity = v
            if (affinity > 0.01):
                affinity = str(affinity)
                word_identifier = word + "-JJ-1"
                RelatePersonDescribedbyDescriptor(graph,person_identifier,word_identifier,affinity)

########################### Initializing ##########################

# Initialize Config

config = ConfigParser.ConfigParser()
config.read('config.ini')

# Initialize Logger
LOGGER_FILEPATH = config.get('Logging','LOGGER_FILEPATH')
LOGGER_DEBUG_FILEPATH = config.get('Logging','LOGGER_DEBUG_FILEPATH')

logger = logging.getLogger('UntitledLogger.DBUtils')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(LOGGER_FILEPATH)
fh.setLevel(logging.WARNING)

debugfh = logging.FileHandler(LOGGER_DEBUG_FILEPATH)
debugfh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
debugfh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(debugfh)

logger.info('Logging Started for DBUtils.')
