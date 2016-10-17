import os
from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch import Elasticsearch, RequestsHttpConnection
import json
from django.views.decorators.http import require_GET
from requests_aws4auth import AWS4Auth
from django.conf import settings

# AWS Elasticsearch node
ES_NODE = "search-tweetmap-2bov3qumzzffrdtz4zezla675m.us-west-2.es.amazonaws.com"

def load_credentials(filename):
    """
    Load AWS and Twitter Credentials
    """
    with open(filename) as handle:
        credentials = json.load(handle)
        # _twitter_creds = credentials["twitter"]
        _aws_creds = credentials["aws"]["kunal"]

        # return _twitter_creds, _aws_creds
        return _aws_creds

# Load AWS credentials
CRENDENTIAL_FILE = os.path.join(settings.BASE_DIR, "TweetMapp/secret/key.json")
aws_creds = load_credentials(CRENDENTIAL_FILE)

#AWS auth for elasticsearch
awsauth = AWS4Auth(aws_creds['ACCESS_KEY'], aws_creds['SECRET_KEY'], "us-west-2", "es")

#elasticsearch client
es = Elasticsearch(hosts=[{'host': ES_NODE, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection)

@require_GET
def index(request):
	#return HttpResponse("Welcome to Tweet-Mapp, Embed a Map here")
	return render(request, 'TweetMapp/index.html')


@require_GET
def wordsearch(request):
    '''
        Gets text string for search
        returns list of {"id":[lat, lng]} mappings
    '''
    tweets = dict()
    if request.GET['query'] == '':
        # query elasticsearch
        result = es.search(index="tweetmap", size=10000, body={"query": {"match_all": {}}})
        for hit in result['hits']['hits']:
            location = hit['_source']['location']
            tweets[hit['_id']] = [location['lat'], location['lon']]

    return HttpResponse(json.dumps(tweets), content_type="application/json")