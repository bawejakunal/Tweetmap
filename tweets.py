#!/usr/bin/env python
"""
    Collect Tweets from Twitter
"""
import tweepy
import json
import time
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

ES_NODE = "search-tweetmap-2bov3qumzzffrdtz4zezla675m.us-west-2.es.amazonaws.com"

def load_credentials(filename):
    """
    Load AWS and Twitter Credentials
    """
    with open(filename) as handle:
        credentials = json.load(handle)
        _twitter_creds = credentials["twitter"]
        _aws_creds = credentials["aws"]["kunal"]

        return _twitter_creds, _aws_creds

#loading credentials
twitter_creds, aws_creds = load_credentials("key.json")

#Twitter auth
twitter_auth = tweepy.OAuthHandler(twitter_creds['CONSUMER_KEY'], twitter_creds['CONSUMER_SECRET'])
twitter_auth.set_access_token(twitter_creds['ACCESS_TOKEN'], twitter_creds['ACCESS_TOKEN_SECRET'])

#Twitter API object
twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=5)

#AWS auth
awsauth = AWS4Auth(aws_creds['ACCESS_KEY'], aws_creds['SECRET_KEY'], "us-west-2", "es")

#elasticsearch client
es = Elasticsearch(hosts=[{'host': ES_NODE, 'port': 443}],
                   http_auth=awsauth,
                   use_ssl=True,
                   verify_certs=True,
                   connection_class=RequestsHttpConnection)


class StreamListener(tweepy.StreamListener):
    """
        Stream Listener
    """
    def on_data(self, data):
        """
            On proper status
        """
        try:
            json_data = json.loads(data)
            if json_data['coordinates'] is not None:
                location = json_data['coordinates']['coordinates']
                document = {
                    'text': json_data['text'],
                    'location': {
                        'lat': location[1],
                        'lon': location[0]
                    }
                }

                es.create(index="tweetmap",
                          doc_type="tweet", id=json_data['id'],
                          body=document, ttl="2m")

        except (KeyError, UnicodeDecodeError, Exception) as e:
            pass

    def on_error(self, status_code):
        """
            handle error of listener
        """
        if status_code == 420:
            print "YOU ARE BEING RATE LIMITED"
            return False  #Disconnect stream


def create_index():
    """
        create mapping of data
    """
    mappings = '''
    {
        "tweet":{
            "_ttl":{
                "enabled": true,
                "default": "2m"
            },
            "properties": {
                "text":{
                    "type": "string"
                },
                "location":{
                    "type": "geo_point"
                }
            }
        }
    }
    '''
    # Ignore if index already exists
    es.indices.create(index='tweetmap', ignore=400, body=mappings)



def main():
    """
        main method of script
    """
    create_index()
    stream_listener = StreamListener()
    try:
        streamer = tweepy.Stream(twitter_api.auth, listener=stream_listener)
        streamer.filter(locations=[-180, -90, 180, 90], languages=['en'])
    except Exception as e:
        print e
        raise Exception(e)
    # Ideally we should try catch exception here
    # but we put a hack to throw outside program which is catched by our bash script to restart the script

if __name__ == '__main__':
    main()
