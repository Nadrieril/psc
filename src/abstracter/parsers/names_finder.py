##########################################"
##UNUSED

"""
To give an idea of what we need (and how use freebase), I reproduce below 
a code from https://gist.github.com/jackschultz/6701521
"""

import nltk
import string
import requests
import operator
import re
import logging
#from collections import defaultdict
from nltk import word_tokenize, sent_tokenize, pos_tag

pattern = '[A-Z][^A-Z]*'
FREEBASE_API_KEY = "AIzaSyBPhRSY6Q1iPx82tnkoWAzbAc4JqhNjiJs"

class FindNames(object):
 
  def __init__(self, text, freebase_api_key):
    self.text = text#.encode('ascii','ignore')
    self.key = freebase_api_key
    self.valid_mids = []
    self.sentences = self._get_sentences()
    self.unnamed_entities = self._get_named_entities()
    self.topic_dict = defaultdict(int)
    self.searched_domains = set()
    self.freebase_search_url = 'https://www.googleapis.com/freebase/v1/search'
    self.freebase_mqlread = 'https://www.googleapis.com/freebase/v1/mqlread'
    self.freebase_topic_url = 'https://www.googleapis.com/freebase/v1/topic'
    self.useless_domains = set(['/common','/people','/user', '/base', '/location', '/organization']) #don't give information...
 
 
  def _get_sentences(self):
    '''
    Strip sentences from the text. Better way since newlines were screwing it up.
    Also removes "'s" from things. All text cleaning should go hear before
    processing.
    '''
    nlsplit=sent_tokenize(self.text)
    #nlsplit = [l.strip() for l in self.text.split('\n')]
    sents = []
    for para in nlsplit:
      #for s in nltk.tokenize.sent_tokenize(para):
        #interesting here. We know it won't go past the 's, so we need a split up token.
      sents.append(para.replace("'s",","))
    return sents
 
  def _get_named_entities(self):
    '''
    Returns a list of the named entities found in the text initially
    '''
    named_entities = []
    tot = set()
    for sent in self.sentences:
      split = nltk.word_tokenize(sent)
      tokens = nltk.pos_tag(split)
      temp = []
      for key,val in tokens:
        if val == 'NNP' and len(key) >= 3 and key[0].istitle(): #make sure uppercase too
          temp.append(key)
        else:
          if temp:
            cap_list = re.findall(pattern, ''.join(temp))
            tot.add(tuple(temp))
            if len(cap_list) >= 2:
              #also want to check if the thing is just letters
              ngs = nltk.ngrams(cap_list,2)
              for n in ngs:
                #sometimes we get acronyms, don't want that
                if not any([len(word)==1 for word in n]):
                  tot.add(n)
            temp = []
      if temp:
        tot.add(tuple(temp))
    named_entities = []
    #string the phrases
    for ph in tot:
      named_entities.append(' '.join(ph))
    #alittle better, but better text needed
 
    return named_entities
 
  def get_people(self):
    '''
    We go through the list of named_entities and we attempt to identify
    them using Freebase.
    '''
    #loop goes searches for people without domain, we remove those
    #entities from the list, get the best domain, and then search
    #again with the filter. Later extensions should work to both
    #use the domain filters to pick off topic, and other non-person
    #entities in the text.
    changes = True
    domain = None
    num_runs = 3
    print('Found following Named Entities:')
    print(self.unnamed_entities)
    changes = self._search_freebase(domain)
    dom_ind = 0
    domain = self._get_domain(dom_ind)
    self.searched_domains.add(domain)
    changes = self._search_freebase(domain)
    #_get_domain returns none if out of ind
    self._print_valid_names()
    return self.valid_mids
 
  def _search_freebase(self, domain=None):
    '''
    We want to search the unnamed entities with the domain specified
    '''
    scores = []
    ratios = []
    print('Searching on domain: ' + str(domain))
    params = {}
    params['key'] = self.key
    if domain:
      params['filter'] = '(any type:/people/person domain:' + domain + ')'
    else:
      params['filter'] = '(any type:/people/person)'
    mids = []
    test_entities = self.unnamed_entities[:]
    for ne in test_entities:
      params['query'] = ne
      options = requests.get(self.freebase_search_url, params=params).json().get("result", "")
      #TODO seperate scoreing function to make cleaner and and better than this naive model
      if len(options) >= 2:
        ratios.append((options[0].get('score')/options[1].get('score'),ne))
        scores.append((options[0].get('score'),ne))
        if options[0].get('score') > 2 * options[1].get('score')  \
              and options[0].get('score') > 100                   \
              and nltk.metrics.edit_distance(ne, options[0].get('name')) < 3: #don't know optimal distance yet
          #levinshtein distance!! We can get some odd ones otherwise
          mids.append((ne,options[0].get('mid'),options[0].get('name')))
      elif len(options) == 1 and options[0].get('score') > 100    \
              and nltk.metrics.edit_distance(ne, options[0].get('name')) < 3: #don't know optimal distance yet
        scores.append((options[0].get('score'),ne))
        mids.append((ne,options[0].get('mid'),options[0].get('name')))
      else: #remove if don't even return a result
        self.unnamed_entities.remove(ne)
    return self._resolve_people(mids)
 
  def _resolve_people(self, mids):
    '''
    We want to check if the mids are people. mids is a list of tuples so we know what
    guess mid relates to the ne
    '''
    print('Checking for people...')
    fin_mids = []
    params = {}
    any_valid = False
    for mid_tup in mids:
      mid = mid_tup[1]
      common_mql = '''
            "*": null,
            "type": [{
              "id": null,
              "domain": []
            }]
      '''
      query_mql = '{"id":"' + mid + '",' + common_mql.replace(' ','').replace('\n','') + '}'
      fburl = self.freebase_mqlread + '?query=' + query_mql + '&key='+self.key
      result = requests.get(fburl)
      if result.status_code == 200: #maybe it's a string
        #now we go throught and get the types and the domains... TODO use notable instead of all domains
        type_list = []
        domain_list = []
        for info in result.json()['result']['type']:
          type_list.append(info['id'])
          try:
            domain_list.append(info['domain'][0])
          except IndexError: #sometimes there is no domain
            continue
      else:
        logging.warning('Freebase returned non 200 code when asking for types...skipping this MID')
        continue
      if u'/people/person' in type_list:
        #want to get the domains now
        any_valid = True
        for domain in domain_list:
          if not any([el == 0 for el in [domain.find(x) for x in self.useless_domains]]):
            self.topic_dict[domain] += 1
        self.unnamed_entities.remove(mid_tup[0])
        self.valid_mids.append(mid_tup)
        fin_mids.append(mid_tup)
    self._show_people_names(fin_mids)
    return any_valid
 
  def _show_people_names(self,mids):
    print('Found these names this round:')
    for mid in mids:
      print(mid[0] + ' ---> ' + mid[2])
 
  def _get_domain(self, ind):
    '''
    This gets the higest ranked domain from topic dict
    '''
    sorted_topics = sorted(self.topic_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    try:
      return sorted_topics[ind][0]
    except IndexError:
      return None
 
  def _print_valid_names(self):
    for name in self.valid_mids:
      print(name)
 
  def get_freebase_info(self, mid):
    '''
    Gets topic info for an mid. Should do better error checking in future
    '''
    params = {}
    params['key'] = self.key
    return requests.get(self.freebase_topic_url+mid, params=params).json()
 
def main():
  '''
  Run some tests
  '''
  fn = FindNames(text, FREEBASE_API_KEY)
  print(fn.get_people())
 
if __name__ == '__main__':
 
  text = '''
Peyton Manning will have a new left tackle protecting his blindside after the Denver Broncos placed Ryan Clady on season-ending injured reserve Wednesday.

Clady hurt his left foot Sunday when New York Giants defensive lineman Cullen Jenkins rolled up on him while the Broncos were trying to run out the clock in their 41-23 win. Clady will soon undergo surgery for what's being called a Lisfranc tear, which involves a separation of ligaments and joints in the foot.

Chris Clark, a fifth-year journeyman, will take the place of Clady - the undisputed leader on the line - and make his first career start at left tackle Monday night when the Broncos (2-0) host the Oakland Raiders (1-1).

''Stepping up into a role like this, it's not going to be hard for me to adjust,'' said Clark, who received a two-year contract extension on Monday. ''It's not about filling a guy's shoes for me. It's about me creating my legacy, just helping the team the best way I can and doing my job.''

Still, those are some big cleats for Clark to fill.

After all, Clady has been a mainstay at left tackle, never missing a start since being selected in the first round in 2008 out of Boise State. He allowed just one sack last season, the fewest in the NFL. By keeping Manning so safe and secure, Clady made his third Pro Bowl team and was voted an All-Pro first-teamer for the second time in his career.

The Broncos also rewarded his protection of Manning by signing him to a five-year deal in July worth up to $57.5 million. Clady was slowed during training camp as he recovered from offseason shoulder surgery.

Over the years, Clark has been paying close attention to Clady's stellar technique, preparing just in case a day like this ever arrived.

''Just the way he moves, the way he sets, the way he moves his feet and hands, attention to detail. You try to mimic those things because he's been a great player and those things will help me a lot,'' Clark said of his understudy role. ''It helps me being here, practice, games, whatever - it helps a lot.''

This isn't the first time the Broncos have had to reshuffle the offensive line in front of Manning. Earlier this summer, the team lost center Dan Koppen for the year to an ACL injury. The offense hasn't missed a beat with Manny Ramirez snapping the ball to Manning, averaging 45 points a game.

''You want your quarterback to feel comfortable when he's back there, knowing that the person that's responsible for that is going to make the right calls and the right adjustments when the time comes,'' said Ramirez, who also signed a two-year extension last week. ''I think I've filled that role so far and I'm just going to continue to improve it.''

To fill Clady's spot, the Broncos brought in veteran tackle Winston Justice, who played last season in Indianapolis after spending six years in Philadelphia. The 6-foot-6, 317-pound Justice has started 43 games in his career, including one at left tackle.
  
  '''
 
main()