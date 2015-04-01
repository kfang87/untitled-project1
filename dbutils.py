import logging
import ConfigParser

from py2neo import Graph, Relationship

import untitledutils


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
        logger.info("Person node created successfully for %s.", identifier)
    except:
        logger.warning("Problem with creating person {}", identifier)
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
        logger.info("Descriptor node created successfully for %s.", desciptor_meaning_identifier)
    except:
        logger.warning("Problem with creating descriptor {}", word)
    return descriptor

def CreateCharacterTrait(graph, word):
    try:
        trait = graph.merge_one("Trait", "word", word.lower())
        trait.push()
        logger.info("Trait node created successfully for %s.", word)
    except:
        logger.warning("Problem with creating trait {}", word)
    return trait

def CreateName(graph, firstname):
    try:
        name = graph.merge_one("Name","base_name",firstname)
        name.push()
        logger.info("Name node created successfully for %s.", firstname)
    except:
        logger.warning("Problem with creating name for {}", firstname)
    return firstname

# Relationship functions

def RelatePersonHasName(graph, person_identifier, base_name):
    try:
        person = graph.find_one("Person", "identifier", person_identifier)
        name = graph.find_one("Name", "base_name",base_name)
        r = Relationship(person, "HAS_NAME", name)
        graph.create_unique(r)
        r.push()
        logger.info("Relationship HAS_NAME created between {} and {}",person_identifier, base_name)
    except:
        logger.warning("Problem with creating relationship between {} and {}",person_identifier, base_name)

def RelatePersonDescribedbyDescriptor(graph, person_identifier, descriptor_word_identifier, confidence_pct):
    try:
        person = graph.find_one("Person", "identifier", person_identifier)
        descriptor = graph.find_one("Descriptor", "descriptor_meaning_identifier", descriptor_word_identifier)
        r = Relationship(person, "DESCRIBED_BY", descriptor, confidence=confidence_pct)
        graph.create_unique(r)
        r.push()
        logger.info("Relationship DESCRIBED_BY created between {} and {}", person_identifier, descriptor_word_identifier)
    except:
        logger.warning("Problem with creating relationship between {} and {}", person_identifier, descriptor_word_identifier)

def RelateDescriptorSimilartytoTrait(graph, descriptor_word_identifier, trait_word, similarity_pct):
    try:
        descriptor = graph.find_one("Descriptor", "descriptor_meaning_identifier", descriptor_word_identifier)
        trait = graph.find_one("Trait","word", trait_word.lower())
        r = Relationship(descriptor, "IS_SIMILAR_TO", trait, similarity=similarity_pct )
        graph.create_unique(r)
        r.push()
        logger.info("Relationship IS_SIMILAR_TO created between {} and {}", descriptor_word_identifier, trait_word)
    except:
        logger.warning("Problem with creating relationship between {} and {}", descriptor_word_identifier, trait_word)


def update_database():


    documents = untitledutils.get_documents()
    graph = getGraph()

    # Get all words from file
    vocabulary =  untitledutils.load_vocabulary()
    docterm_matrix_dict, vocabulary_dict = untitledutils.create_doc_term_importance(documents, vocabulary)

    # BUILD THE GRAPH

    # TODO: build NAME
    for doc in documents:
        CreateName(graph, untitledutils.get_name_from_docname(doc))
    #     print 'Name: ' + HumanName(entity).first

    # TODO: build DESCRIPTOR
    for word in vocabulary_dict.iterkeys():
        CreateDescriptor(graph,word)
    #     print 'Descriptor: ' + word
    #
    # TODO: build CHARACTER TRAIT
    characteristics_file = open('C:\code\untitled-project1\data\character_traits.txt')
    characteristics_file.readline()
    characteristics_array = characteristics_file.read().split('\n')
    characteristics_file.close()
    for char in characteristics_array:
        CreateCharacterTrait(graph,char)

    # TODO: build relationships between PERSON and NAME
    for doc in documents:
        RelatePersonHasName(graph, doc.replace(".txt",""),  untitledutils.get_name_from_docname(doc))
    #
    # TODO: build relationships between DESCRIPTOR and CHARACTER TRAIT
    for char in characteristics_array:
        for word in vocabulary_dict:
            result = untitledutils.calculate_word_similarity(word, char)
            if (result > 0.05):
                RelateDescriptorSimilartytoTrait(graph,word + "-JJ-1", char, result)

    # # TODO: build relationships between PERSON and DESCRIPTOR
    for item in vocabulary_dict.iterkeys():
        index_of_word =  vocabulary_dict[item]
        word_docmatrix = docterm_matrix_dict.getcol(index_of_word)
        for doc_index in range(0,documents.__len__()):
            person_identifier = documents[doc_index].replace(".txt","")
            word = str(item.encode('utf-8'))
            affinity_matrix = word_docmatrix.getrow(doc_index).values()
            if affinity_matrix.__len__() > 0:
                affinity = str(affinity_matrix[0])
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
