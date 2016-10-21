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
    '''
        Welcome page
    '''
    return render(request, 'TweetMapp/index.html')

@require_GET
def fetchtweet(request):
    '''
        Fetch Tweet by id
    '''
    tweet_id = request.GET['id']
    tweet = 'Tweet Not Found !!!'

    try:
        result = es.get(index="tweetmap", id=tweet_id)
        tweet = result['_source']['text']
    except Exception as e:
        print e
    
    return HttpResponse(tweet, content_type="text/plain")


@require_GET
def wordsearch(request):
    '''
        Gets text string for search
        returns list of {"id":[lat, lng]} mappings
    '''
    tweets = dict()
    query = dict()

    # Empty string treated as match_all
    query_str = str(request.GET['query'])

    # Query DSL for elastic search
    query = {'match': 
                {'text':{
                    'query':query_str,
                    'zero_terms_query': "all"
                    }
                }
            }
    
    result = es.search(index="tweetmap", filter_path=['hits.hits._id', 'hits.hits._source.location'], size=10000, body={"query": query})

    try:
        for hit in result['hits']['hits']:
            location = hit['_source']['location']
            tweets[hit['_id']] = [location['lat'], location['lon']]

    except KeyError:
        print "No Results found"

    return HttpResponse(json.dumps(tweets), content_type="application/json")