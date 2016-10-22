# Tweetmap

<a href=http://tenk-env.33qgpym9us.us-west-2.elasticbeanstalk.com/>10K Tweets - Geovisualization of Real-Time Twitter Data</a>


We have built a simple web application that maps tweets to their location in real time. We used <a href=http://www.tweepy.org/> Tweepy</a>, which is an easy-to-use Python library for accessing the Twitter API. Initially, we pull ten thousand tweets and store them on the <a href= https://aws.amazon.com/elasticsearch-service/> Amazon Elasticsearch Service</a>. Elasticsearch provides the benefit of easily scaling our clusters through single API calls or the management console. Furthermore, it can automatically replace failed Elasticsearch nodes, reducing the overhead associated with self-managed infrastructure like ours. 


Our application is built using <a href=https://www.djangoproject.com/Django> Django</a> which is a powerful Python Web framework. We have utilized the Google Maps API for plotting the tweet clusters. On the server-side, we pull tweet information using Tweepy and store them in Elasticsearch. Then we query Elasticsearch every 5 seconds in order to obtain tweet/location data in the Json format. We render this data on the client-side in the form of markers that appear and disappear in real time. At any point of time, the map contains atmost 10K tweets. This limitation follows from the fact that Elasticsearch only allows a maximum of 10K tweets to be stored at any given time. We deploy our application on top of <a href = http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.html>AWS Elastic Beanstalk</a> which does an excellent job, handling details such as load balancing, scaling, and application monitoring. 


##Usage:
Tweets can be filtered using keywords which are typed into a textbox. We've used <a href=http://www.w3schools.com/bootstrap/bootstrap_get_started.asp>Bootstrap</a>, a front-end framework that easily creates responsive designs like buttons, forms etc. In addition, we use JQuery AJAX methods for exchanging (tweet/loc) Json data with the server, and for updating only specific parts of the web page. The markers indicate locations from where the tweets were posted. If we click on a marker, it displays real-time tweets in the form of strings. 
