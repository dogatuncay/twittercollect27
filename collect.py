__author__ = 'DogaT'

import oauth2 as oauth
import urllib2 as urllib
import json
import re

consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
http_method = "GET"

http_handler = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)


def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url,
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)


  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response


def haspositive(text):

    emoticons = [':-)', ':)', '=)', ':-D', ':D', '8-D', 'xD', '8D', 'x-D', 'X-D', 'XD', ":'-)", ';D', ":')", ':*',
                 ';-)', ';)', ':P', '=P', ':]', '=D']

    for emoticon in emoticons:
        if text.find(emoticon) > -1:
            return True
    return False

def hasnegative(text):

    emoticons = [':-(', ':(', ':[', '=(', ":'-(", ":'(", '=/', ':/']

    for emoticon in emoticons:
        if text.find(emoticon) > -1:
            return True
    return False

def retrievetweets():

    pos = open('C:/Users/DogaT/Desktop/tweets/positive.txt', 'a')
    neg = open('C:/Users/DogaT/Desktop/tweets/negative.txt', 'a')

    url = "https://stream.twitter.com/1/statuses/sample.json"
    parameters = []
    response = twitterreq(url, "GET", parameters)

    for line in response:
        jtweet = json.loads(line)

        if "text" in jtweet and "lang" in jtweet and jtweet["lang"] == 'en':
            tweet = (jtweet["text"]).encode('utf-8'), "\n"
            tweet = ' '.join(tweet)
            tweet = tweet.replace("\n", " ")
            tweet = re.sub(r"http\S+", "", tweet)

            if haspositive(tweet):
                pos.write("\n" + tweet)
                print(tweet)
            if hasnegative(tweet):
                neg.write("\n" + tweet)
                print(tweet)
        pos.flush()
        neg.flush()
    pos.close()
    neg.close()

if __name__ == '__main__':
    retrievetweets()
