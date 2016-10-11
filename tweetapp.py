import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import os
import io


#Peruse Read.me on how to obtain the security key and access token. This basically allows read/write operations to your twitter profile
# through API using Python.
consumer_key='lzwiLyivUX2yS0ZQHHwGjLBwJ'
consumer_secret='rTyp7xLV7i8NagYJal5FF6DxYxd6I7yatu8xlv4w5FPAANDJ1z'
access_token = '824965753-jb9i3FSKeuvC4bptwA7wHKBVRNZ78gaXhXqfYECf'
access_token_secret= 'u2IwaTAdPQJsUQVRnLUgOumDudYpmjopIsvQGqMdN17Su'


start_time=time.time() #Start time of listener, set to system time

keyword_list=['italy'] # we only get tweets that contain these keywords. NOTE: Cannot have spaces.



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



#status = "Testing times!"                  # This lets you post a status on your twitter timeline. Try it!
#api.update_status(status=status)

#public_tweets = api.home_timeline()       # this prints all the tweets on your timeline. Try it
#for tweet in public_tweets:
 #   print tweet.text


#Now we need to override the ondata method of mylistener which is a subclass of StreamListener. The ondata method is called when tweet data is received
#What we do with the data is dependent on how we override this method.
class mylistener(tweepy.StreamListener):
	def __init__(self, start_time, time_limit=60):
 
		self.time = start_time
		self.limit = time_limit
		self.tweet_data = []
 
	def on_data(self, data):
 
		saveFile = io.open('raw_tweets_italy.json', 'a', encoding='utf-8') # creates file where we want our tweets stored
 
		while (time.time() - self.time) < self.limit: #Get tweets for 20 secs
 
			try:
 
				self.tweet_data.append(data) # keep appending data to tweet_data list
 
				return True
 
 
			except BaseException, e:
				print 'failed ondata,', str(e)
				time.sleep(5)
				pass
 
		saveFile = io.open('raw_tweets_italy.json', 'w', encoding='utf-8')
		saveFile.write(u'[\n')
		saveFile.write(','.join(self.tweet_data))
		saveFile.write(u'\n]')
		saveFile.close()
		exit()
 
	def on_error(self, status):
 
		print statuses
 
twitterStream = Stream(auth, mylistener(start_time, time_limit=40)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en']) #filter tweets to only gets the ones with the desired keywords