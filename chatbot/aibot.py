import nltk
import string
#from project.settings import BASE_DIR
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def usr_response(user_request):
    f=open('vaccine-facts.txt','r',errors = 'ignore')
    raw = f.read()

    nltk.download('punkt')
    nltk.download('wordnet')

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
        sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]

        if (req_tfidf == 0):
            robo_response = robo_response + "I am sorry! I don't understand you"
            return robo_response
        else:
            robo_response = robo_response + sent_tokens[idx]
            return robo_response

    return response(user_request)