import logging
import os
import ConfigParser
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from requests import get
import nltk


########################## Sourcing utilities ##########################
def create_person_document(entityname, content):
    logger = logging.getLogger('UntitledLogger.SourceUtilities')
    
    DOCUMENT_FILEPATH = config.get('Sourcing','DOCUMENT_FILEPATH')
    filename = entityname + '.txt'
    filepath = os.path.join(DOCUMENT_FILEPATH, filename)

    try:
        if (os.path.isfile(filepath) and os.path.getsize(filepath) > 0):
            logger.info('File already exists at %s, skipping file creation', filepath)
        else:
            with open(filepath,'w') as f:
                f.write(content)
            logger.info('Creating context file %s for entity %s', filepath, entityname)
    except:
        logger.error('Could not complete creating file for filepath %s, %s',filename,sys.exc_info()[0])

    return filepath


########################## Name Term Frequency utilities ##########################
    
#given a set of documents, create a matrix that represents the importance of a term within a document
# def create_doc_term_importance(docs):
#     logger.info('Beginning Document-Term frequency analysis')
#     countvectorizer = CountVectorizer(input='filename', stop_words='english', encoding='ascii',decode_error='replace',analyzer='word',token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b")
#     countvectorizer.fit(docs)
#     wordcount_matrix = countvectorizer.transform(docs)
#
#     # # Construct tfidf values sparse matrix of [documents, vocabulary]
#     tfidf_transformer = TfidfTransformer(smooth_idf=True).fit(wordcount_matrix)
#     tfidf_matrix = tfidf_transformer.transform(wordcount_matrix)
#     logger.info('Finished creating tdidf matrix')
#     return tfidf_matrix, countvectorizer.vocabulary_

########################### Initializing ##########################
def calculate_word_similarity(word1, word2):
    try:
        sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
        return float(get(sss_url, params={'operation':'api','phrase1':word1,'phrase2':word2}).text.strip())
    except:
        return 0.0




def create_doc_term_importance(docs, vocabulary):
    countvectorizer = CountVectorizer(input='filename', stop_words='english', encoding='ascii',decode_error='replace',analyzer='word',token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z]+\b",vocabulary=vocabulary)
    wordcount_matrix = countvectorizer.fit_transform(docs)
    # # Construct tfidf values sparse matrix of [documents, vocabulary]
    tfidf_transformer = TfidfTransformer(smooth_idf=True).fit(wordcount_matrix)
    tfidf_matrix = tfidf_transformer.transform(wordcount_matrix)
    return tfidf_matrix, countvectorizer.vocabulary_

def get_adj_vocabulary(docs):
    vocabulary = set()
    for doc in docs:
        with open(doc) as f:
            text = f.read().decode(encoding='utf-8',errors='ignore')
            for sentence in nltk.sent_tokenize(text):
                pos = nltk.pos_tag(nltk.word_tokenize(sentence))
                for (word,tag) in pos:
                    if tag == "JJ" and not vocabulary.__contains__(word):
                        vocabulary.add(word)
    return vocabulary
########################### Initializing ##########################

# Initialize Config

config = ConfigParser.ConfigParser()
config.read('config.ini')

# Initialize Logger
LOGGER_FILEPATH = config.get('Logging','LOGGER_FILEPATH')
LOGGER_DEBUG_FILEPATH = config.get('Logging','LOGGER_DEBUG_FILEPATH')

logger = logging.getLogger('UntitledLogger')
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
