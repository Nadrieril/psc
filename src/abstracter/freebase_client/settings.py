#settings for freebase_client

#personal key used for retrieving freebase information
#google knows who we are...
USER_KEY="AIzaSyBPhRSY6Q1iPx82tnkoWAzbAc4JqhNjiJs"

#minimum score
MINIMUM_RESULT_SCORE=100

#basis url for searching
URL='https://www.googleapis.com/freebase/v1/search'

#query : "wayne rooney" domain :"/sport" lang: "en"

#domain : restrict to topics with this freebase domain id
#encode : html or off

#exact : boolean query on exact name and keys only
#filter : make complex queries using the symbols
#all, any, should not  : operators
#type domain name alias with without : operands
# () parenthesis
#indent : indent json results or not
#lang : default is 'en'
#limit : default is 20
#spell : 'did you mean' suggestions ; always, no_results, no_spelling (default)
#scoring : string : relevance scoring algo to use : entity (default), freebase, schema
#format :string:  entity (default), ids (freebase ids), mids (freebase mids)
SEARCH_PARAMETERS=['as_of_time','callback','cursor','domain'
,'encode','exact','filter','format','indent','lang','limit'
,'mql_output','prefixed','query','scoring','spell','stemmed','type','with','without']
