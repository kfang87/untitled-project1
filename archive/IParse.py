import abc


class IParse(object):
    __metaclass__ = abc.ABCMeta
    
    #given a set of documents, create a matrix that represents the importance of a term within a document
    @abc.abstractmethod
    def create_doc_term_importance(self, docs):
        return
    
    #given document-term importance matrix, aggregate important terms for given name
    @abc.abstractmethod
    def extract_relevant_context(self, rawsource, context):
        return
