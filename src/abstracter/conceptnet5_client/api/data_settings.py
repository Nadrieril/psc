#useful edges with associated weight
#these weights are arbitrary
USEFUL_CONCEPTNET_EDGES = { '/r/IsA' : 1,
'/r/CapableOf' : 0.4,
'/r/AtLocation' : 0.7,
'/r/Antonym' : 0.3,
'/r/HasProperty' : 0.9,
'/r/HasA' : 0.8,
'/r/UsedFor' : 0.4,
}

NOT_USEFUL_CONCEPTNET_EDGES = ['/r/NotCapableOf','/r/ReceivesAction','/r/RelatedTo','/r/Desires']

MINIMUM_WEIGHT_ALLOWED = 0.5#which is weight of the edge in conceptnet5 * arbitrary 
#weight to keep most important information
#for example, (/c/en/dog -> /r/CapableOf -> /c/en/sense_fear , 3) is not relevant
#(/c/en/dog -> /r/HasA -> /c/en/fur , 4) is relevant
#(/c/en/dog -> /r/RelatedTo -> /c/en/pet , 4) is very relevant

#maximum number of underscores in a relevant concept
#with more than 2 underscores, the concept has more than 3 words and is most unlikely to find 
#in a text
MAX_UNDERSCORES_ALLOWED=2

#warning : some of these attributes do not exist in conceptnet5.3
ALL_EDGES_ATTRIBUTES=['start','startLemmas','rel','end','endLemmas','weight','score','uri','nodes',
'text','features','sources','context','dataset','timestamp']
RELEVANT_EDGES_ATTRIBUTES=['start','rel','end','weight']