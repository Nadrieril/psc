from abstracter.crawler.parse_crawler import download_and_parse_data,unify

#download_and_parse fait tout pour une date : télécharger sur le crawler, 
#stocker localement les données, parser les articles 
#et faire des listes de concepts + de noms
#il crée aussi de nouveaux fichiers dans concepts_names_data

download_and_parse_data("2015_01_17")
#download_and_parse_data("2015_01_14")
#unify()


#print(search_name("barack obama"))
#print(cn.search_concept("barack_obama"))

#import abstracter.parsers.retriever as re


#print(re.retrieve_words_names(text))