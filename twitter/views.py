from django.shortcuts import render, redirect

import twitter
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
# import unicodedata2
# import urllib
import simplejson
##import json
import sys

# import nltk.classify.util
# from nltk.classify import NaiveBayesClassifier
# from nltk.corpus import names
# from nltk.corpus import stopwords
import numpy as np
from matplotlib import pylab


# Create your views here.

def home(request):
    return render(request, 'homepage.html', {})


def checkForm(request):
    errors = []
    url = request.POST['url']
    reply = request.POST['replies']

    if url == '':
        errors.append("Please enter URL")

    if reply == '':
        errors.append("Please enter number of replies")

    if len(errors) == 0:
        return render(request, 'homepage.html', {})
    else:
        return redirect('/', errors)
        # return render(request, 'homepage.html', {'errors': errors})



def twitterAuth(request):
    try:
        auth = OAuthHandler(settings.consumer_key, settings.consumer_secret)
        auth.set_access_token(settings.access_token, settings.access_token_secret)
        api = tweepy.API(self.auth, wait_on_rate_limit=True)
    except:
        print("Error: Authentication Failed")
        

def sentiments(request):
    return render(request, 'sentiment.html', {})
