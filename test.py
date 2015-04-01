__author__ = 'Kayla'
import untitledutils
import ntpath
import scipy.sparse
import itertools

documents = untitledutils.get_documents()
# Get all words from file
vocabulary =  untitledutils.load_vocabulary()
docterm_matrix, vocabulary_dict = untitledutils.create_doc_term_importance(documents, vocabulary)

index = 0
for i,j,v in zip(docterm_matrix.row, docterm_matrix.col, docterm_matrix.data):
    person_identifier = ntpath.basename(documents[i]).replace(".txt","")
    word = str(vocabulary_dict[j]).encode('utf-8')
    affinity = v
    if (affinity > 0.01):
        affinity = str(affinity)
        word_identifier = word + "-JJ-1"
        RelatePersonDescribedbyDescriptor(graph,person_identifier,word_identifier,affinity)


#
# for item in vocabulary_dict.iterkeys():
#     index_of_word =  vocabulary_dict[item]
#     word_docmatrix = docterm_matrix_dict.getcol(index_of_word)
#     for doc_index in range(0,documents.__len__()):
#         person_identifier = ntpath.basename(documents[doc_index]).replace(".txt","")
#         word = str(item.encode('utf-8'))
#         affinity_matrix = word_docmatrix.getrow(doc_index).values()
#         if affinity_matrix.__len__() > 0:
#             affinity = str(affinity_matrix[0])
