__author__ = 'Kayla'
import logging
import ConfigParser
import urllib2
from BeautifulSoup import BeautifulSoup

config = ConfigParser.ConfigParser()
config.read('config.ini')

def retrieve_name_meaning(name):
    url = config.get('External','NAME-MEANINGS-URL') + name
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        meaning = soup.find("td",{"class" : "meaning"}).text.strip()
        info = soup.find("td",{"class" : "gender"})
        gender = info.contents[0].replace('Gender:','').strip()
        origin = info.contents[2].replace('Origin:','').strip()
        return {'meaning': meaning, 'gender': gender, 'origin' : origin }
    except Exception as e:
        logging.warning("Problem with retrieving name meaning for name %s: %s", name, e.message)
