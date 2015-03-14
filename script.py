from SourceWikipedia import SourceWikipedia
import untitledutils
import scipy.sparse
from nameparser import HumanName

source = SourceWikipedia()
entities = source.retrieve_sourcelist('List_of_female_scientists_before_the_21st_century', 5)

documents = []

document_entities_dict = {}

# for pageid in entities:
#     data = source.retrieve_data_from_source(pageid)
#     entity, context, uri = source.extract_relevant_context(data)
#     filename = untitledutils.create_person_document(entity, context)
#     personal_name = HumanName(entity)
#     document_entities_dict[filename] = entity
#     documents.append(filename)

for title in entities:
    data = source.retrieve_data_from_source(title)
    entity, context, uri = source.extract_relevant_context(data)
    if (context):
        filename = untitledutils.create_person_document(entity, context)
        personal_name = HumanName(entity)
        document_entities_dict[filename] = entity
        documents.append(filename)

docterm_matrix, vocabulary_dict = untitledutils.create_doc_term_importance(documents)
docterm_matrix_dict = scipy.sparse.dok_matrix(docterm_matrix)

# TODO: build PERSON
for entity in document_entities_dict.itervalues():
    print 'Person: ' + entity

# TODO: build DESCRIPTOR
for word in vocabulary_dict.iterkeys():
    print 'Descriptor: ' + word

# TODO: build CHARACTER TRAIT
characteristics_file = open('C:\code\untitled-project1\data\character_traits.txt')
characteristics_file.readline()
characteristics_array = characteristics_file.read().split('\n')
characteristics_file.close()

for char in characteristics_array:
    print 'Character Trait: ' + char

# TODO: build NAME
for entity in document_entities_dict.itervalues():
    print 'Name: ' + HumanName(entity).first

# TODO: build relationships between PERSON and NAME
person_name_dict = {}
for entity in document_entities_dict.itervalues():
    print 'The entity ' + entity + ' has a name of ' + HumanName(entity).first

# TODO: build relationships between PERSON and DESCRIPTOR
for item in vocabulary_dict.iterkeys():
    index_of_word =  vocabulary_dict[item]
    word_docmatrix = docterm_matrix_dict.getcol(index_of_word)
    for doc_index in range(0,documents.__len__()-1):
        docname = documents[doc_index]
        word = str(item.encode('utf-8'))
        affinity_matrix = word_docmatrix.getrow(doc_index).values()
        if affinity_matrix.__len__() > 0:
            affinity = str(affinity_matrix[0])
            print document_entities_dict[docname] + ' can be described as ' + word + ' with the confidence of ' + affinity


# TODO: build relationships between DESCRIPTOR and CHARACTER TRAIT
for char in characteristics_array:
    for word in vocabulary_dict:
        result = untitledutils.calculate_word_similarity(word, char)
        if (result > 0.01):
            #place holder for inserting into Neo4J
            print ('The similarity between ' + word + ' and ' + char + ' is ' + str(result)).encode('utf8')
