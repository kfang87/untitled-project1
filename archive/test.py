from archive import dbutils

# documents = []
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Achelous.txt')
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Acheron.txt')
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Adonis.txt')
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Aegipan.txt')
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Aeolus.txt')
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Aesepus.txt')
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Aether (mythology).txt')
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Aethon.txt')
# documents.append('C:\Temp\UntitledProject-Workspace\EntityDocuments\Agathodaemon.txt')
#
# docterm_matrix, vocabulary_dict = untitledutils.create_doc_term_importance(documents)
# docterm_matrix_dict = scipy.sparse.dok_matrix(docterm_matrix)
#
# characteristics_file = open('C:\code\untitled-project1\data\character_traits.txt')
# characteristics_file.readline()
# characteristics_array = characteristics_file.read().split('\n')
# characteristics_file.close()
#
# with open('similarity.txt','a') as out:
#     for char in characteristics_array:
#         for word in vocabulary_dict:
#             result = untitledutils.calculate_word_similarity(word, char)
#             if (result > 0.01):
#                 # out.write(('The similarity between ' + word + ' and ' + char + ' is ' + str(result)).encode('utf8') + '\n')
#                 print ('The similarity between ' + word + ' and ' + char + ' is ' + str(result)).encode('utf8')
# out.close()

        # print ('The similarity between ' + word + ' and ' + char + ' is ' + str(untitledutils.calculate_word_similarity(word, char))).encode('utf8') + '\n'
# print docterm_matrix_dict

# for item in vocabulary_dict:
#     index =  vocabulary_dict[item]
#     col = docterm_matrix_dict.getcol(index)
#     print item.encode('utf8') + ': ' + str(col.todense())
    # with open('data.txt','a') as out:
    #     out.write(item.encode('utf8') + ': ' + str(col.todense()))

graph = dbutils.getGraph()

dbutils.CreatePerson(graph,"Alice","Alice Johnson")