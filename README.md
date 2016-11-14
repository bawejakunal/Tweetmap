#Tweetmap

[10K Tweets - Geovisualization of Real-Time Twitter Data](http://cloudwebapp-env.zrsgmaburw.us-west-2.elasticbeanstalk.com/)

**Deployment URL**: [http://cloudwebapp-env.zrsgmaburw.us-west-2.elasticbeanstalk.com/](http://cloudwebapp-env.zrsgmaburw.us-west-2.elasticbeanstalk.com/)

**About**

A simple web application that does the following:
1. Visualizes upto 10,000 tweets on world map in real time using their geolocation data.
2. Search tweets by keywords
3. Geospatial search - click on a point in map to see all tweets originating from a 1000 mile radius around the point.

**Dependencies**

1. [Tweepy v3.5.0](http://www.tweepy.org/) - a python library to connect and use [Twitter API](https://dev.t. witter.com/)

2. [AWS Elasticsearch v2.3](https://aws.amazon.com/elasticsearch-service/) - store and analyze tweets to enable realtime search and mapping

3. [Google Maps v3.0 API](https://developers.google.com/maps/documentation/javascript/reference) - display world map and use markers to plot tweets

4. [ElasticSearch Python Client](https://elasticsearch-py.readthedocs.io) - connect to elasticsearch server node programatically

5. [AWS4Auth](https://pypi.python.org/pypi/requests-aws4auth) - handle user authentication via OAuth2 protocol for using AWS services

6. Read [requirements.txt](requirements.txt) for further details.

**Description**

This simple project captures all geotagged tweets from the twitter streaming API and stores them in our elasticsearch instance deployed in the AWS cloud infrastructure. For indexing tweets into elasticsearch domain we store three main fields from the tweet data that we get from twitter streaming API:

1. Tweet ID

2. Tweet text (actual content of tweet)

3. Tweet geolocation (latitude and longitude)

Our front page for visualization is served from a simple [django server](https://www.djangoproject.com/Django) application deployed in an auto-scaling environment of AWS Elasticbeanstalk, which provides easy scaling for our application in case of changes in traffic, both scaling up and scaling down the required resources.

**Using 10K Tweets**

1. Visit [http://tenk-env.33qgpym9us.us-west-2.elasticbeanstalk.com](http://tenk-env.33qgpym9us.us-west-2.elasticbeanstalk.com)

2. Click any point on the map to view all tweets from 1000 mile radius of that point.

3. Search your favourite keywords in the search box to visualize relevant tweets on the world map.

4. Click on a map marker to view the tweet content

5. The map is refreshed every 10 seconds to display latest tweets relevant to the keywords tracked via search box

**Details for newbies**

This application is built using [Django](https://www.djangoproject.com/Django) which is a powerful Python Web framework. We have utilized the Google Maps API v3.0(https://developers.google.com/maps/documentation/javascript/reference) for plotting the tweet clusters. On the server-side, we pull tweet information using [Tweepy](http://www.tweepy.org/) and store them in [AWS Elasticsearch](https://aws.amazon.com/elasticsearch-service/) server. Then we query [AWS Elasticsearch](https://aws.amazon.com/elasticsearch-service/) every 10 seconds in order to obtain new tweet/location data in the JSON format. We render this data on the client-side in the form of markers that appear and disappear on the map in real time. At any point of time, the map contains at most 10K tweets. This limitation follows from the fact that pulling too much data into browser makes the browser busy and hangs up the view, which we can further optimize in the future iterations of this project.

We deploy our application on top of [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) which does an excellent job, handling details such as load balancing, scaling, and application monitoring automagically.
