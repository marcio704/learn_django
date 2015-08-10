import sys
import models
from enum import Enum
from django.conf import settings
from elasticsearch import Elasticsearch


class ElasticSearchClient():
	es = Elasticsearch()
	
	def __init__(self):
		pass

	def insert_document(self, id, json_document, document_type):
		res = self.es.index(index=settings.ELASTIC_SEARCH_INDEX, doc_type=document_type.value, id=id, body=json_document)

	def search_post_by_match(self, text):
		query = {
			"query": {
				"bool": {
					"should": [
						{ "match": { "text":  text }},
						{ "match": { "resume":  text }},
		        		{ "match": { "title": {"query": text, "boost": 2} }}
		      		]
		    	}
		  	},
		  	"highlight": { 
		  		"pre_tags" :  ["<b> <i> <ins>"],
        		"post_tags" : ["</ins> </i> </b> "], 
        		"fields" : { "text" : {}, "resume": {}, "title": {} } 
        	}
		}

		res = self.es.search(index=settings.ELASTIC_SEARCH_INDEX, doc_type=DocumentType.post.value, body=query)
		post_list = []
		for hit in res['hits']['hits']:
			post = models.Post.objects.get(pk=hit["_source"]["id"])
			try:
				post.title = hit["highlight"]["title"][0]
			except:
				post.title = hit["_source"]["title"]
			try:
				post.resume = hit["highlight"]["resume"][0]
			except:
				post.resume = hit["_source"]["resume"]
			try:
				post.text = hit["highlight"]["text"][0]
			except:
				post.text = ""

			post_list.append(post)

		return post_list

class DocumentType(Enum):
	post = "post"
	commentary = "commentary"