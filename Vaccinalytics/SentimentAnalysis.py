import tweepy
from textblob import TextBlob
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
nltk.download('punkt')

#function to get subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

#get polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

def cleanText(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text) #remove hyperlink
    return text

#function to obtain general sentiment
def getAnalysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"


#Variables that contain user credentials to access Twitter API
consumer_key = "JQvK453l06Y7wbJ68pRSginjL"
consumer_key_secret = "cekE914GJszQ9CAzKqnSIZ1ZkcWMRgWfPmWmWrBSm51cfLPAku"
bearer_token = "AAAAAAAAAAAAAAAAAAAAANfsMAEAAAAAZY6HGt1XwP0Bx8AWqR%2BUjlGs4u4%3DgJSaePMGzsk3TSHSFXlaSlcXKN2csQ0yU5I5m9bVyC6jzBnKYV"
access_token = "743874915716075521-85JUHDZlr1wlCm4jI0k4JqxiIusYmQc"
access_token_secret = "IyvFsOKAVj3ehpJfI6eZPuvOnRsASAMuYTn1ZyWBQrjta"


#obtaining tweets using API
search_words = "#CovidVaccine" + " -filter:retweets"
date_since = "2021-01-02"
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

tweets = tweepy.Cursor(api.search,q=search_words,lang="en",since=date_since).items(5000)

all_tweets = [tweet.text for tweet in tweets]
print(len(all_tweets))

df = pd.DataFrame(all_tweets, columns = ['Tweets'])

df['Tweets'] = df['Tweets'].apply(cleanText)


#create columns in df
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)


df['Analysis'] = df['Polarity'].apply(getAnalysis)

allWords = ' '.join([twts for twts in df['Tweets']])

for i in range(0, df.shape[0]):
    plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color="Green")

df.to_csv("covidtweets.csv", sep = ',')


#get percentage of positive tweets
ptweets = df[df.Analysis == "Positive"]
ptweets = ptweets["Tweets"]

features_positive = [(f,
           'Positive') for f in ptweets]

#get percentage of negative tweets
ntweets = df[df.Analysis == "Negative"]
ntweets = ntweets["Tweets"]
features_negative = [(f,'Negative') for f in ntweets]

# Split the data into train and test (80/20)
threshold_factor = 0.8
threshold_pos = int(threshold_factor * len(features_positive))
threshold_neg = int(threshold_factor * len(features_negative))

features_train = features_positive[:threshold_pos] + features_negative[:threshold_neg]
features_test = features_positive[threshold_pos:] + features_negative[threshold_neg:]
print("\nNumber of training datapoints:", len(features_train))
print("Number of test datapoints:", len(features_test))

all_words = set(word.lower() for passage in features_train for word in word_tokenize(passage[0]))
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in features_train]

test_words = set(word.lower() for passage in features_test for word in word_tokenize(passage[0]))
t1 = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in features_test]
print("breakpoint 14")
classifier = NaiveBayesClassifier.train(t)
print("\nAccuracy of the classifier:", nltk.classify.util.accuracy(classifier, t1))

print("\nTop 20 most informative words:")
for item in classifier.most_informative_features()[:20]:
    print(item[0])
