import nltk
import string
from pathlib import Path

from scrape_tweets import get_tweets

from scipy import spatial
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent


def qna_response():
    tweet_list = get_tweets()
    response_list = []
    for tweet in tweet_list:
        f = open(str(BASE_DIR) + '/fact_checker/vaccine-facts.txt', 'r', errors='ignore')
        raw = f.read()

        # nltk.download('punkt')
        # nltk.download('wordnet')

        sent_tokens = nltk.sent_tokenize(raw)

        WNL = nltk.stem.WordNetLemmatizer()

        def LemTokens(tokens):
            return [WNL.lemmatize(token) for token in tokens]

        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

        def LemNormalize(text):
            return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

        LemNormalize(sent_tokens[0])

        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)

        # function to match input to the preprocessed sentences
        def response(user_response):
            robo_response = ''
            new = TfidfVec.transform([user_response])
            vals = cosine_similarity(new[0], tfidf)
            idx = vals.argsort()[0][-1]
            idx_2 = vals.argsort()[0][-2]
            idx_3 = vals.argsort()[0][-3]
            flat = vals.flatten()
            flat.sort()
            req_tfidf = flat[-1]
            if req_tfidf == 0:
                robo_response = robo_response + "unable to find answer, please rephrase your question."
                return robo_response
            else:
                robo_response = robo_response + sent_tokens[idx] + sent_tokens[idx_2] + sent_tokens[idx_3]
                return {'robo_response': robo_response, 'single_sentence_token': sent_tokens[idx]}

        user_response = response(tweet['tweet'])
        response_dictionary = {'msg': user_response['robo_response'].replace("\n", ""), 'tweet_url': tweet['tweet_url'], 'screenshot': tweet['screenshot']}

        model = SentenceTransformer('paraphrase-distilroberta-base-v1')

        sentences = [tweet['tweet'],
                     user_response['single_sentence_token']]
        sentence_embeddings = model.encode(sentences)

        dist = spatial.distance.cosine(sentence_embeddings[0], sentence_embeddings[1])
        print('dist_1: {0}'.format(dist))

        if dist > 0.30:
            response_dictionary['tweet_type'] = 'myth'
        else:
            response_dictionary['tweet_type'] = 'fact'

        response_list.append(response_dictionary)
    return {'tabular_list': response_list}
