__author__ = 'Kayla'
from nameparser import HumanName
import ntpath
from requests import get
from os import listdir
import string
from HTMLParser import HTMLParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import scipy.sparse
import logging
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

def get_name_from_docname(docname):
    docname = ntpath.basename(docname)
    if docname.__contains__("_"):
        name = HumanName(docname[0:docname.index("_")].replace("-"," ")).first.capitalize()
    else:
        name = HumanName(docname).first.capitalize()
    return name


def calculate_word_similarity_swoogle(word1, word2):
    try:
        sss_url = config.get('External','SWOOGLE_SIMILARITY_URL')
        sim = get(sss_url, params={'operation':'api','phrase1':word1 + "_JJ",'phrase2':word2 + "_JJ",'type':'relation'},).text.strip()
        return float(sim)
    except:
        return 0.0

def load_vocabulary():
    vocabulary_set = set()
    with open(config.get('Data','VOCAB_FILEPATH'),'r') as f:
        vocabulary_set = f.read().splitlines()
    logging.info("Vocabulary set loaded successfully with %s words", vocabulary_set.count())
    return vocabulary_set

def get_documents():
    documents = []
    dir = config.get('Data','ENTITIES_FILEPATH')
    for file in listdir(unicode(dir,'utf-8')):
        documents.append(dir + "\\" + file)
    logging.info("Successfully retrieved %s documents from %s", documents.__len__(), dir)
    return documents

def create_entity_identifier(fullname,source):
    p = HTMLParser()
    exclude = set(string.punctuation)
    fullname = ''.join(ch for ch in p.unescape(fullname) if ch not in exclude)
    source = ''.join(ch for ch in p.unescape(source) if ch not in exclude)
    return (fullname + "_" + source).replace(" ","-").lower()

def create_doc_term_importance(docs, vocabulary):
    countvectorizer = CountVectorizer(input='filename', stop_words='english', encoding='ascii',decode_error='replace',analyzer='word',token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",vocabulary=vocabulary)
    wordcount_matrix = countvectorizer.fit_transform(docs)
    tfidf_transformer = TfidfTransformer(smooth_idf=True).fit(wordcount_matrix)
    tfidf_matrix = tfidf_transformer.transform(wordcount_matrix)
    return scipy.sparse.coo_matrix(tfidf_matrix), countvectorizer.get_feature_names()

