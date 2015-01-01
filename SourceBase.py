import abc


class SourceBase(object):
    __metaclass__ = abc.ABCMeta
    
    #given a URI, gets the raw returned value from the source
    @abc.abstractmethod
    def retrieve_data_from_source(self, sourceuri):
        return
    
    #given the raw source, extracts the relevant context
    @abc.abstractmethod
    def extract_relevant_context(self, rawsource, context):
        return
