#https://developers.google.com/freebase/v1/search-cookbook



#settings for freebase_client

#personal key used for retrieving freebase information
#google knows who we are...
USER_KEY="AIzaSyDT_kRl5YXKUlha-RkH71-ojQRWLK69Xf4"
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
#mid : machine id
SEARCH_PARAMETERS=['as_of_time','callback','cursor','domain'
,'encode','exact','filter','format','indent','lang','limit'
,'mql_output','prefixed','query','scoring','spell','stemmed','type','with','without']

#filter operands
#filter: "(all type:battles tookplace_at:marengo)"
FILTER_OPERANDS=['abstraction','abstraction_of',
'adaptation',
'administered_by',
'administers',
'appears_in',
'broader_than',
'category',
'center',
'center_for',
'certification',
'character',
'child',
'contributed_to',
'contributor',
'created',
'created_by',
'discovered',
'discovered_by',
'distributed_by',
'exhibited',
'exhibited_at',
'expressed_by',
'fictional_link',
'genre',
'identifies',
'leader',
'leader_of',
'made_of',
'means_of_demise',
'member_of',
'narrower_than',
'occurs_in',
'origin',
'owner',
'owns',
'parent',
'part_of',
'participant',
'participated_in',
'peer_of',
'permits_use_of',
'portrayed',
'portrayed_by',
'practitioner_of',
'preceeding',
'produced_by',
'publication',
'publication_of',
'service_area',
'status',
'subclass_of',
'subject',
'subsequent',
'succeeded_by',
'succeeds',
'superclass_of',
'title',
'tookplace_at',
'use_permitted_by',
]
