import pandas as pd
from pathlib import Path

import tweepy
from nltk.tokenize import word_tokenize

BASE_DIR = Path(__file__).resolve().parent.parent


# Variables that contain user credentials to access Twitter API
consumer_key = "JQvK453l06Y7wbJ68pRSginjL"
consumer_key_secret = "cekE914GJszQ9CAzKqnSIZ1ZkcWMRgWfPmWmWrBSm51cfLPAku"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANfsMAEAAAAAZY6HGt1XwP0Bx8AWqR%2BUjlGs4u4" \
               "%3DgJSaePMGzsk3TSHSFXlaSlcXKN2csQ0yU5I5m9bVyC6jzBnKYV "
access_token = "743874915716075521-85JUHDZlr1wlCm4jI0k4JqxiIusYmQc"
access_token_secret = "IyvFsOKAVj3ehpJfI6eZPuvOnRsASAMuYTn1ZyWBQrjta"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


def get_tweets():
    tmp = []
    
    df = pd.read_csv(str(BASE_DIR)+'/fact_checker/tweets.csv', header=None)

    for index, row in df.iterrows():
        tweets = api.user_timeline(screen_name=row[0], count=1)
        tweets_for_csv = [tweet.text for tweet in tweets]
        for t in tweets_for_csv:
            if 'vaccine' or 'vaccinated' in word_tokenize(t):
                tmp.append({'tweet': t, 'username': row[0], 'tweet_url': row[1], 'screenshot': str(BASE_DIR)+row[2]})
    return tmp
