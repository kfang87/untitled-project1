from wikitools import api, wiki
import simplejson as json

searchterm = 'Greek_gods'
limit = 100
sourceuri = 'http://en.wikipedia.org/w/api.php'

params = {'action':'query',
    'list' : 'categorymembers',
    'cmtitle' : 'Category:' + searchterm,
    'cmprop' : 'ids',
    'cmtype' : 'page',
    'cmlimit' : limit        
}

site = wiki.Wiki(sourceuri)
request = api.APIRequest(site, params)
res = request.query(querycontinue=False)
json_str = json.dumps(res, ensure_ascii=False).encode('utf8')
dict = json.loads(json_str)


entity_list = []

parent = dict["query"]["categorymembers"]

for item in parent:
    entity_list.append( item[u'pageid'] )
    
for pageid in entity_list:
    print 'pageid: ' + str(pageid)