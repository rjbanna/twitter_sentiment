from django.shortcuts import render, redirect
from django.conf import settings

import re
import tweepy
import requests
from tweepy import OAuthHandler
from textblob import TextBlob
from collections import Counter

import validators
# Create your views here.

def home(request):
    return render(request, 'homepage.html', {})


def checkForm(request):
    errors = []
    url = request.POST['url']
    reply = request.POST['replies']
    return redirect('sentiments', url= url, reply=reply)

    if url == '':
        errors.append("Please enter URL")

    if reply == '':
        errors.append("Please enter number of replies")

    if len(errors) == 0:
        return redirect('sentiments')
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

        is_valid = validators.url(url)

        if is_valid:
            fetched_tweets = api.search(q = url, count=count)

            emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF" u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF" "]+", flags=re.UNICODE)

            tweet_replies = []
            for status in fetched_tweets:
                tweet_replies.append((status._json).get('text'))

            for reply in tweet_replies:
                parsed_tweet = {}
                txt = emoji_pattern.sub(r'',reply)
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

            sentiments_list = []
            for tweet in tweets:
                sentiments_list.append(tweet['sentiment'])

            sentiments_list_length = len(sentiments_list)

            counts = Counter(sentiments_list)
            positive = counts['positive']
            neutral = counts['neutral']
            negative = counts['negative']

            positive_percent = round((positive*100)/sentiments_list_length, 2)
            neutral_percent = round((neutral*100)/sentiments_list_length, 2)
            negative_percent = round((negative*100)/sentiments_list_length, 2)

            sentiment_dict = {'Positive': positive_percent, 'Neutral': neutral_percent, 'Negative': negative_percent}

            key_list = list(sentiment_dict.keys())
            value_list = list(sentiment_dict.values())

            overall_sentiment = key_list[value_list.index(sorted([positive_percent, neutral_percent, negative_percent])[-1])]
            sentiment_percent = sentiment_dict[overall_sentiment]

            return render(request, 'sentiment.html', {'is_valid': is_valid, 'data': sentiment_dict, 'overall_sentiment': overall_sentiment.capitalize(), 'sentiment_percent':sentiment_percent })

        else:
            return render(request, 'sentiment.html', {'is_valid': is_valid })

    else:
        return redirect('/')
