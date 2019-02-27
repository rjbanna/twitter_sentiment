from django.shortcuts import render, redirect
from django.conf import settings

import sys
import twitter
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import simplejson
import numpy as np
from matplotlib import pylab

# import unicodedata2
# import urllib
# import json
# import nltk.classify.util
# from nltk.classify import NaiveBayesClassifier
# from nltk.corpus import names
# from nltk.corpus import stopwords


# Create your views here.

def home(request):
    return render(request, 'homepage.html', {})


def checkForm(request):
    errors = []
    url = request.POST['url']
    reply = request.POST['replies']
    return render(request, 'homepage.html', {'errors': url})
    # return render(request, 'sentiment.html', {'d': request.POST})

    if url == '':
        errors.append("Please enter URL")

    if reply == '':
        errors.append("Please enter number of replies")

    if len(errors) == 0:
        return render(request, 'homepage.html', {})
    else:
        return redirect('/', errors)
        return render(request, 'homepage.html', {'errors': errors})



def twitterAuth():
    try:
        auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api
    except:
        return False


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))

    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def sentiments(request):
    if twitterAuth():
        tweets = []
        api = twitterAuth()
        data = request.POST
        url = data['url']
        count = data['replies']

        fetched_tweets = api.search(q ="@"+url)

        # return render(request, 'sentiment.html', {'data': fetched_tweets })

        emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)

        for status in fetched_tweets:
            parsed_tweet={}



            return render(request, 'sentiment.html', {'data': status._json })
            txt = emoji_pattern.sub(r'',status.text)
            txt = txt.lower()
            txt = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?\S', '', txt)
            txt = re.sub(r'#','', txt)
            txt = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",txt).split())

            if txt!='' or txt==None:
                parsed_tweet['text']=txt
                parsed_tweet['sentiment'] = get_tweet_sentiment(txt)

                if len(tweets)>0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

        ptweets=[tweet for tweet in tweets if tweet['sentiment']=='positive']
        ntweets=[tweet for tweet in tweets if tweet['sentiment']=='negative']
        netweets=[tweet for tweet in tweets if tweet['sentiment']=='neutral']

        positive=(len(ptweets)/len(tweets))*100
        negative=(len(ntweets)/len(tweets))*100
        neutral=(len(netweets)/len(tweets))*100


        return render(request, 'sentiment.html', {'data': negative })
    else:
        return redirect('/')
