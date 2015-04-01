import abc
import logging
import string
from ISource import ISource
import ConfigParser
from BeautifulSoup import BeautifulSoup
import urllib2
import untitledutils
import dbutils

logger = logging.getLogger('UntitledLogger.SourceLogger')
config = ConfigParser.ConfigParser()
config.read('config.ini')
        
class SourceSparknotes(object):

    # get content from page, return context for each character
    def retrieve_data_from_source(self, base_url):
        character_chunk_list = []
        url = base_url + '/canalysis.html'
        source_text = ''
        try:
            page = urllib2.urlopen(url)
            if (page.getcode() == 200):
                self.logger.info("Page at %s retrieved successfully",url)
                soup = BeautifulSoup(page)
                character_chunks = soup.findAll("div",{"class" : "content_txt"})
                source_text = soup.find("h1",{"class" :"title padding-btm-0"}).text
                for chunk in character_chunks:
                    character_chunk_list.append(chunk)
        except:
            self.logger.warning("Could not open URL %s", url)
        return character_chunk_list, source_text

    # given content for a character, extract name, context
    def extract_relevant_context(self, content):
        soup = BeautifulSoup(str(content))
        person_name = soup.h4.text
        context = soup.p.text
        self.logger.info("Retrieved content for person %s.", person_name)
        return person_name, context
    
    def retrieve_sourcelist(self):
        urls = []
        #letters = ['h']
        letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for letter in letters:
            url = 'http://www.sparknotes.com/lit/index_' + letter + '.html'
            try:
                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page)
                entrylist = soup.findAll("div",{"class" : "entry"})
                for entry in entrylist:
                    entry_soup = BeautifulSoup(str(entry))
                    if (len(entry_soup.p.a['href']) > 0):
                        urls.append(entry_soup.p.a['href'])
            except:
                self.logger.warning("Could not open url %s", url)
            self.logger.info('Finished retrieving list of urls. List contains %s entries, starting with %s', str(len(urls)), str(urls[0]))
        return urls


    def __init__(self):
        self.logger = logging.getLogger('UntitledLogger.SourceLogger')
        documents = []
        url_list = self.retrieve_sourcelist()
        graph = dbutils.getGraph()

        #url_list = ['http://www.sparknotes.com/lit/potter7/']
        for url in url_list:
            character_chunk_list, source_text = self.retrieve_data_from_source(str(url))
            for character_chunk in character_chunk_list:
                person_name, context = self.extract_relevant_context(character_chunk)
                filename = untitledutils.create_person_document(graph, person_name, context, source_text)
                documents.append(filename)
        return documents
            
ISource.register(SourceSparknotes)
