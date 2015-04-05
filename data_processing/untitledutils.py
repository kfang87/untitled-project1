import logging
import os
import ConfigParser
import nltk
from nameparser import HumanName
from data_processing import dbutils
import enchant


def clean_entity(entity):
    return entity.lower().replace(" ", "-")

def clean_name(name):
    return name.lower().replace(" ", "-")

def get_first_name(fullname):
    return HumanName(fullname).first

def delete_person(person_identifier):
    entities_folder = 'C:\Temp\UntitledProject-Workspace\EntityDocuments'
    filepath = os.path.join(entities_folder,person_identifier + ".txt").decode('utf-8')
    if os.path.exists(filepath):
        os.remove(filepath)
    dbutils.RemovePerson(person_identifier)

def merge_persons(source_person_identifier, target_person_identifier, new_person_fullname, new_person_source_text):
    # add text from source to target, delete source file
    entities_folder = 'C:\Temp\UntitledProject-Workspace\EntityDocuments'
    source_file = os.path.join(entities_folder,source_person_identifier + ".txt").decode('utf-8')
    target_file = os.path.join(entities_folder,target_person_identifier + ".txt").decode('utf-8')

    if (os.path.exists(source_file) and os.path.exists(target_file)):
        with open(target_file,'a') as t:
            with open (source_file, 'r') as s:
                t.write(s.read().decode(encoding='utf-8',errors='ignore') + '\n')
        os.remove(source_file)

    # update the node attributes from source to target, delete source node
    dbutils.MergePersonNodes(source_person_identifier,target_person_identifier, new_person_fullname, new_person_source_text)


def get_adj_vocabulary(docs):
    logger.info("Starting to build vocabulary with documents")
    vocabulary = set()
    all_text = ''
    processor_count = 0
    english_dictionary = enchant.Dict("en_US")
    try:
        for doc in docs:
            with open(doc) as f:
                text = f.read().decode(encoding='utf-8',errors='ignore')
                all_text += "\n" + text
        for sentence in nltk.sent_tokenize(all_text):
            pos = nltk.pos_tag(nltk.word_tokenize(sentence))
            for (word,tag) in pos:
                word = word.lower()
                if tag == "JJ" and not vocabulary.__contains__(word) and english_dictionary.check(word):
                    vocabulary.add(word)
                    with open('..\\data\\vocabulary.txt','a') as f:
                        f.write(word + "\n")
                    processor_count += 1
                    if processor_count % 25 == 0:
                        logger.info("So far, have added %s words to the vocabulary.", processor_count)
    except:
        logger.warning("Failed to open and parse %s", doc)
    logger.info("Completed vocabulary building with a dictionary of %s adjectives", vocabulary.__len__())
    return

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



