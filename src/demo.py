from abstracter.crawler.parse_crawler import download_and_parse_data,unify


download_and_parse_data("2015_01_16")
#download_and_parse_data("2015_01_14")
#unify()

from abstracter.freebase_client import search_name
from abstracter.conceptnet5_client.api import api as cn


#print(search_name("barack obama"))
#print(cn.search_concept("barack_obama"))