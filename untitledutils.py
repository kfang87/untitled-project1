import logging
import os
import ConfigParser
import sys
import string
from HTMLParser import HTMLParser
import ntpath
from os import listdir

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from requests import get
import nltk
from nameparser import HumanName
import scipy.sparse

import dbutils


########################## Sourcing utilities ##########################
def create_person_document(graph, person_name, context, source_text):

    DOCUMENT_FILEPATH = config.get('Sourcing','DOCUMENT_FILEPATH')
    entity_identifier = create_entity_identifier(person_name,source_text)
    filename = entity_identifier + '.txt'
    filepath = os.path.join(DOCUMENT_FILEPATH, filename)

    try:
        if (os.path.isfile(filepath) and os.path.getsize(filepath) > 0):
            logger.info('File already exists at %s, skipping file creation', filepath)
        else:
            with open(filepath,'w') as f:
                f.write(context)
            logger.info('Creating context file %s for entity %s', filepath, person_name)
            #add to database
        dbutils.CreatePerson(graph,entity_identifier, person_name,source_text)
    except:
        logger.error('Could not complete creating file for filepath %s, %s',filename,sys.exc_info()[0])

    return filepath


def clean_entity(entity):
    return entity.lower().replace(" ", "-")

def clean_name(name):
    return name.lower().replace(" ", "-")

def get_first_name(fullname):
    return HumanName(fullname).first

def get_name_from_docname(docname):
    docname = ntpath.basename(docname)
    logger.info("Retreiving name for document " + docname)
    name = HumanName(docname[0:docname.index("_")].replace("-"," ").decode(encoding='utf-8',errors='ignore')).first.capitalize()
    logger.info("Name is " + name)
    return name

def create_entity_identifier(fullname,source):
    p = HTMLParser()
    exclude = set(string.punctuation)
    fullname = ''.join(ch for ch in p.unescape(fullname) if ch not in exclude)
    source = ''.join(ch for ch in p.unescape(source) if ch not in exclude)
    return (fullname + "_" + source).replace(" ","-").lower()

def calculate_word_similarity(word1, word2):
    try:
        sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
        return float(get(sss_url, params={'operation':'api','phrase1':word1 + "_JJ",'phrase2':word2 + "_JJ"}).text.strip())
    except:
        return 0.0

def get_documents():
    documents = []
    dir = "C:\Temp\UntitledProject-Workspace\EntityDocuments"
    for file in listdir(dir):
        documents.append(dir + "\\" + file)
    return documents


def create_doc_term_importance(docs, vocabulary):
    countvectorizer = CountVectorizer(input='filename', stop_words='english', encoding='ascii',decode_error='replace',analyzer='word',token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",vocabulary=vocabulary)
    wordcount_matrix = countvectorizer.fit_transform(docs)
    # # Construct tfidf values sparse matrix of [documents, vocabulary]
    tfidf_transformer = TfidfTransformer(smooth_idf=True).fit(wordcount_matrix)
    tfidf_matrix = tfidf_transformer.transform(wordcount_matrix)

    docterm_matrix_dict = scipy.sparse.dok_matrix(tfidf_matrix)
    return docterm_matrix_dict, countvectorizer.vocabulary_

def get_adj_vocabulary(docs):
    logger.info("Starting to build vocabulary with documents")
    vocabulary = set()
    all_text = ''
    processor_count = 0
    try:
        for doc in docs:
            with open(doc) as f:
                text = f.read().decode(encoding='utf-8',errors='ignore')
                all_text += "\n" + text
        for sentence in nltk.sent_tokenize(all_text):
            pos = nltk.pos_tag(nltk.word_tokenize(sentence))
            for (word,tag) in pos:
                if tag == "JJ" and not vocabulary.__contains__(word):
                    vocabulary.add(word)
                    with open('vocabulary.txt','a') as f:
                        f.write(word + "\n")
                    processor_count += 1
                    if processor_count % 25 == 0:
                        logger.info("So far, have added %s words to the vocabulary.", processor_count)
    except:
        logger.warning("Failed to open and parse %s", doc)
    logger.info("Completed vocabulary building with a dictionary of %s adjectives", vocabulary.__len__())
    return

def load_vocabulary():
    vocabulary_set = set()
    with open('vocabulary.txt','r') as f:
        vocabulary_set.add(f.readline())

########################### Initializing ##########################

# Initialize Config

config = ConfigParser.ConfigParser()
config.read('config.ini')

# Initialize Logger
LOGGER_FILEPATH = config.get('Logging','LOGGER_FILEPATH')
LOGGER_DEBUG_FILEPATH = config.get('Logging','LOGGER_DEBUG_FILEPATH')

logger = logging.getLogger('UntitledLogger.UntitledUtils')
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

logger.info('Logging Started.')



