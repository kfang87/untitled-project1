import abc
import logging
import string
from ISource import ISource
from wikitools import api, wiki
import simplejson as json
import nltk
from nameparser import HumanName
import untitledutils
import ConfigParser

logger = logging.getLogger('UntitledLogger.SourceLogger')
config = ConfigParser.ConfigParser()
config.read('config.ini')
        
class SourceWikipedia(object):
    global WIKIPEDIA_API 
    WIKIPEDIA_API = config.get('Sourcing','WIKIPEDIA_API_URL')


    def retrieve_data_from_source(self, pageid):
    
        params = {'action':'query',
            'rvprop' : 'content',
            'prop' : 'extracts',
            'explaintext' : 'True',
            'pageids' : pageid,
            'exintro' : True
        }
        site = wiki.Wiki(WIKIPEDIA_API)
        request = api.APIRequest(site, params)
        res = request.query(querycontinue=False)
        self.logger.info('Finished retrieving data for pageid: %s ', str(pageid))
        return res
    
    def extract_relevant_context(self, rawsource):
        
        json_str = json.dumps(rawsource, ensure_ascii=False).encode('utf8')
        json_object = json.loads(json_str)
        context_node = json_object.values()[0].values()[0].values()[0].get("extract")
        context = context_node.encode('utf8')
        name = json_object.values()[0].values()[0].values()[0].get("title")
        #name = HumanName(json_object.values()[0].values()[0].values()[0].get("title"))
        
        self.logger.info('Finished extracting content for %s', name)
        
        return (name, context.lower().translate(None,string.punctuation))
    
    def retrieve_sourcelist(self, searchterm, limit):
                
        params = {'action':'query',
            'list' : 'categorymembers',
            'cmtitle' : 'Category:' + searchterm,
            'cmprop' : 'ids',
            'cmtype' : 'page',
            'cmlimit' : limit        
        }

        site = wiki.Wiki(WIKIPEDIA_API)
        request = api.APIRequest(site, params)
        res = request.query(querycontinue=False)
        json_str = json.dumps(res, ensure_ascii=False).encode('utf8')
        dict = json.loads(json_str)


        entity_list = []

        parent = dict["query"]["categorymembers"]

        for item in parent:
            entity_list.append( item[u'pageid'] )
        self.logger.info('Finished retrieving list of entities for extraction. List contains %s entries, starting with %s', str(len(entity_list)), str(entity_list[0]))
        
        #list of source pageids
        return entity_list

    def __init__(self):
        self.logger = logging.getLogger('UntitledLogger.SourceLogger')
            
ISource.register(SourceWikipedia)