from SourceWikipedia import SourceWikipedia
import untitledutils
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB

source = SourceWikipedia()
entities = source.retrieve_sourcelist('Greek_gods', 10)

documents = []

for pageid in entities:
    data = source.retrieve_data_from_source(pageid)
    entity, context = source.extract_relevant_context(data)
    filename = untitledutils.create_entity_document(entity, context)
    documents.append(filename)

# Construct brute count sparse matrix of [documents, vocabulary]
countvectorizer = CountVectorizer(input='filename', stop_words='english')
countvectorizer.fit(documents)
wordcount_matrix = countvectorizer.transform(documents)

# # Construct tfidf values sparse matrix of [documents, vocabulary]
tfidf_transformer = TfidfTransformer(smooth_idf=True).fit(wordcount_matrix)
tfidf_matrix = tfidf_transformer.transform(wordcount_matrix)

print tfidf_matrix.getrow(0).todense().tolist()[0][0]













# list2 = ['I hate the world', 'hello world my name is kayla']
# count_vect = CountVectorizer()
# X_train_counts2 = count_vect.fit_transform(list2)

# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts2)

# clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

# docs_new = ['hate is love', 'kayla has a world']
# X_new_counts = count_vect.transform(docs_new)
# X_new_tfidf = tfidf_transformer.transform(X_new_counts)

# predicted = clf.predict(X_new_tfidf)

# for doc, category in zip(docs_new, predicted):
    # print doc + ':' + cateogry

# print X_train_counts
# with open('data.txt','w') as outfile:
    # outfile.write('one:' + str(X_train_counts))
# print X_train_counts2
# with open('data2.txt','w') as outfile2:
    # outfile2.write('two:' + str(X_train_counts2))
    
# print X_train_counts.shape
# print X_train_counts

# with open('data2.txt','w') as outfile2:
    # outfile2.write('two:' + str(count_vect.vocabulary_))
# print count_vect.vocabulary_