import logging
import os
import nltk
from nameparser import HumanName
import dbutils
#import enchant
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('config.ini')

def clean_entity(entity):
    return entity.lower().replace(" ", "-")

def clean_name(name):
    return name.lower().replace(" ", "-")

def get_first_name(fullname):
    return HumanName(fullname).first

def delete_person(person_identifier):
    entities_folder = config.get('Data','ENTITIES_FILEPATH')
    filepath = os.path.join(entities_folder,person_identifier + ".txt").decode('utf-8')
    if os.path.exists(filepath):
        os.remove(filepath)
    dbutils.RemovePerson(person_identifier)

def merge_persons(source_person_identifier, target_person_identifier, new_person_fullname, new_person_source_text):
    # add text from source to target, delete source file
    entities_folder = config.get('Data','ENTITIES_FILEPATH')
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
    logging.info("Starting to build vocabulary with documents")
    vocabulary = set()
    total_vocab = 0
    #english_dictionary = enchant.Dict("en_US")
    for doc in docs:
        try:
            with open(doc) as f:
                contributed_vocab = 0
                text = f.read().decode(encoding='utf-8',errors='ignore')
                for sentence in nltk.sent_tokenize(text):
                    pos = nltk.pos_tag(nltk.word_tokenize(sentence))
                    for (word,tag) in pos:
                        word = word.lower()
                        if tag == "JJ" and not vocabulary.__contains__(word):# and english_dictionary.check(word):
                            vocabulary.add(word)
                            with open(config.get('Data','VOCAB_FILEPATH'),'a') as f:
                                f.write(word + "\n")
                            contributed_vocab += 1
                            total_vocab += 1
                logging.info('%s contributed %s vocabulary words for a total of %s words.', doc, contributed_vocab, total_vocab)
        except:
            logging.warning("Failed to open and parse %s", doc)
    logging.info("Completed vocabulary building with a dictionary of %s adjectives", vocabulary.__len__())
    return

