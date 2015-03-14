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
    
    # Retrieves a list of identifiers for entities
    def retrieve_sourcelist(self, searchterm, limit):
        params = {'action':'query',
                  'titles':searchterm,
                  'prop':'links',
                  'pllimit':limit
            #'list' : 'categorymembers',
            #'cmtitle' : 'Category:' + searchterm,
            #'cmprop' : 'ids',
            #'cmtype' : 'page',
            #'cmlimit' : limit
        }

        site = wiki.Wiki(WIKIPEDIA_API)
        request = api.APIRequest(site, params)
        res = request.query(querycontinue=False)
        json_str = json.dumps(res, ensure_ascii=False).encode('utf8')
        dict = json.loads(json_str)


        entity_list = []

        parent = dict["query"]["pages"].values()[0]["links"]

        for item in parent:
            entity_list.append( item[u'title'] )
        self.logger.info('Finished retrieving list of entities for extraction. List contains %s entries, starting with %s', str(len(entity_list)), str(entity_list[0]))

        #list of source pageids
        return entity_list

    
    # #Retrieves raw content from a source object
    # def retrieve_data_from_source(self, pageid):
    #
    #     params = {'action':'query',
    #         'rvprop' : 'content',
    #         'prop' : 'extracts',
    #         'explaintext' : 'True',
    #         'pageids' : pageid,
    #         'exintro' : True
    #     }
    #     site = wiki.Wiki(WIKIPEDIA_API)
    #     request = api.APIRequest(site, params)
    #     res = request.query(querycontinue=False)
    #     self.logger.info('Finished retrieving data for pageid: %s ', str(pageid))
    #     return res

        #Retrieves raw content from a source object
    def retrieve_data_from_source(self, title):

        params = {'action':'query',
            'rvprop' : 'content',
            'prop' : 'extracts',
            'explaintext' : 'True',
            'titles' : title,
            'exintro' : True
        }
        site = wiki.Wiki(WIKIPEDIA_API)
        request = api.APIRequest(site, params)

        try:
            res = request.query(querycontinue=False)
            self.logger.info('Finished retrieving data for title: %s ', str(title))
        except:
            self.logger.info('Failed at retrieving data for title: %s ', str(title))
        return res
    
    #Given raw content from source, returns name and string content
    def extract_relevant_context(self, rawsource):
        
        json_str = json.dumps(rawsource, ensure_ascii=False).encode('utf8')
        json_object = json.loads(json_str)
        context_node = json_object.values()[0].values()[0].values()[0].get("extract")
        context = context_node.encode('utf8')
        entityname = json_object.values()[0].values()[0].values()[0].get("title")
        #name = HumanName(json_object.values()[0].values()[0].values()[0].get("title"))
        
        self.logger.info('Finished extracting content for %s', entityname)
        
        return entityname, context.lower().translate(None,string.punctuation), WIKIPEDIA_API


    def __init__(self):
        self.logger = logging.getLogger('UntitledLogger.SourceLogger')
            
ISource.register(SourceWikipedia)