import logging
import urllib2
from BeautifulSoup import BeautifulSoup
from ISource import ISource
import dbutils
import ConfigParser

class SourceSparknotes(object):

    # get content from page, return context for each character
    def retrieve_data_from_source(self, base_url):
        character_chunk_list = []
        url = base_url + '/canalysis.html'
        source_text = ''
        try:
            page = urllib2.urlopen(url)
            if (page.getcode() == 200):
                logging.info("Page at %s retrieved successfully",url)
                soup = BeautifulSoup(page)
                character_chunks = soup.findAll("div",{"class" : "content_txt"})
                source_text = soup.find("h1",{"class" :"title padding-btm-0"}).text
                for chunk in character_chunks:
                    character_chunk_list.append(chunk)
        except:
            logging.warning("Could not open URL %s", url)
        return character_chunk_list, source_text

    # given content for a character, extract name, context
    def extract_relevant_context(self, content):
        soup = BeautifulSoup(str(content))
        person_name = soup.h4.text
        context = soup.p.text
        logging.info("Retrieved content for person %s.", person_name)
        return person_name, context
    
    def calculate_sourcelist(self):
        letters = ['h']
        #letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

        urls_count = 0

        for letter in letters:
            url = 'http://www.sparknotes.com/lit/index_' + letter + '.html'
            try:
                page = urllib2.urlopen(url)
                soup = BeautifulSoup(page)
                entrylist = soup.findAll("div",{"class" : "entry"})
                for entry in entrylist:
                    entry_soup = BeautifulSoup(str(entry))
                    if (len(entry_soup.p.a['href']) > 0):
                        urls_count += 1
                        with open(self.config.get('Data','URL_FILEPATH'), 'a') as f:
                            f.write(entry_soup.p.a['href'] + "\n")
            except:
                logging.warning("Could not open url %s", url)
            logging.info('Finished retrieving list of urls.')

    def get_sourcelist(self):
        urls = []
        with open(self.config.get('Data','URL_FILEPATH'), 'r') as f:
            urls = f.read().splitlines()
        return urls

    def __init__(self):

        documents = []
        graph = dbutils.getGraph()
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.ini')

        # self.calculate_sourcelist()
        url_list = self.get_sourcelist()

        for url in url_list:
            character_chunk_list, source_text = self.retrieve_data_from_source(str(url))
            for character_chunk in character_chunk_list:
                person_name, context = self.extract_relevant_context(character_chunk)
                filename = dbutils.create_person_document(graph, person_name, context, source_text)
                documents.append(filename)
            
ISource.register(SourceSparknotes)
