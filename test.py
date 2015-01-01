from wikitools import api, wiki
import simplejson as json
import nltk
import string
from collections import Counter
from nltk.corpus import stopwords
import sys
from bs4 import BeautifulSoup
from nltk.stem.porter import *

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(unicode(item, errors='replace')))
    return stemmed

site = wiki.Wiki("http://en.wikipedia.org/w/api.php")
# params = {'action':'query',
    # 'generator':'allpages',
    # 'gaplimit':'10',
    # 'gapfrom':'Barack_Obama',
    # 'prop':'info'
# }
params = {'action':'query',
    'rvprop' : 'content',
    'prop' : 'extracts',
    'explaintext' : 'True',
    'pageids' : 534366,
    'exintro' : True
}

req = api.APIRequest(site, params)
res = req.query(querycontinue=False)
res_raw = json.dumps(res, ensure_ascii=False).encode('utf8')
#print res_raw
data = json.loads(res_raw)
text = data.values()[0].values()[0].values()[0].get("extract")
text2 = text.encode('utf8')
print 'sourcing finished: ' + text2

tokens = nltk.word_tokenize(text2.lower().translate(None,string.punctuation))
filtered = [w for w in tokens if not unicode(w, errors='ignore') in stopwords.words('english')]
print 'tokens'
stemmer = PorterStemmer()
stemmed = stem_tokens(filtered, stemmer)
count = Counter(filtered)
print count.most_common(100)

# with open('data.txt','w') as outfile:
    # json.dump(data, outfile, indent=4)

# print res_raw
# tokens = res_raw.lower().translate(None,string.punctuation)
# print 'tokens'
# count = Counter(tokens)
# print count.most_common(100)