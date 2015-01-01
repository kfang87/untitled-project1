import abc
import string
from SourceBase import SourceBase
from wikitools import api, wiki
import simplejson as json
import nltk

class SourceWikipedia(object):

    def retrieve_data_from_source(self, sourceuri):
    
        params = {'action':'query',
            'rvprop' : 'content',
            'prop' : 'extracts',
            'explaintext' : 'True',
            'pageids' : 534366,
            'exintro' : True
        }
        site = wiki.Wiki(sourceuri)
        request = api.APIRequest(site, params)
        res = request.query(querycontinue=False)
        return res
    
    def extract_relevant_context(self, rawsource):
        json_str = json.dumps(rawsource, ensure_ascii=False).encode('utf8')
        json_object = json.loads(json_str)
        context_node = json_object.values()[0].values()[0].values()[0].get("extract")
        context = context_node.encode('utf8')
        
        return context.lower().translate(None,string.punctuation)
 
SourceBase.register(SourceWikipedia)