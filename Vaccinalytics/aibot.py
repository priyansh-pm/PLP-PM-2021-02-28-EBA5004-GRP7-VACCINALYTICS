import fitz
import nltk
import pyttsx3
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import speech_recognition as sr
import os
import matplotlib

import subprocess
from PyPDF2 import PdfFileReader

from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize


matplotlib.use('Agg')
from matplotlib import pyplot


def listen():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    inp = r.recognize_google(audio)
    print(inp)
    return inp


def qna_response(user_request):
    f = open('vaccinefacts.txt', 'r', errors='ignore')
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
            # robo_response.save('audiobk.mp3')
            return robo_response

    GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
    GREETING_RESPONSES = ["hi", "hey", "hi there", "hello"]

    def greeting(sentence):
        for word in sentence.split():
            if word.lower() in GREETING_INPUTS:
                return random.choice(GREETING_RESPONSES)

    def spf():
        path_to_pdf = os.path.abspath(out + ".pdf")
        # testing this on my Windows Install machine
        process = subprocess.Popen(path_to_pdf, shell=True)
        process.wait()
        #print(out + '.pdf')
        os.remove(out + '.pdf')

    def speak():
        # # Speaking rate
        voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

        # Use female voice
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)  # setting up new voice rate
        engine.setProperty('voice', voice_id)
        # engine.runAndWait()
        # rate = engine.getProperty('rate')  # getting details of current speaking rate
        print('speaking')
        engine.say(bot_response)
        engine.runAndWait()
        engine.stop()



    directory = r'D:\NUS\pytry\chatbot'
    bot_response = ''
    instnce = 0
    j = 0
    substring = "evidence"
    if (substring in user_request):

        user_request = user_request.replace(substring, '')

        #stop words

        sw_list = ['save', 'document', 'protect', 'show', '?', 'could', 'does not', 'covid-19', 'please', 'cure', 'fact']
        all_stopwords = stopwords.words('english')
        print(all_stopwords)
        all_stopwords.extend(sw_list)

        text_tokens = word_tokenize(user_request)
        tokens_without_sw = [word for word in text_tokens if not word in all_stopwords]
        filtered_sentence = (" ").join(tokens_without_sw)
        print(filtered_sentence)
        # Reg_stemmer = RegexpStemmer('s')
        # Reg_stemmer.stem(filtered_sentence)
        # print(filtered_sentence)

        user_request = filtered_sentence
        user_count = len(user_request.split())

        for filename in os.listdir(directory):
            if filename.endswith(".pdf"):
                doc = fitz.open(filename)
                fpath = os.path.join(directory, filename)
                pdf = PdfFileReader(open(fpath, 'rb'))
                pno = pdf.getNumPages()
                print(filename, pno)
                pno = pno - 1
                count = 0
                for i in range(pno-1):

                    # if(j==0):

                    page = doc[i]
                    # print("Processing page: " + str(i))
                    j = i
                    count = 0

                    ### SEARCH

                    text = user_request
                    text_instances = page.searchFor(text)

                    ###trial
                    x = user_request.split()
                    # user_request_text = page.searchFor(x[0])
                    # for i in range(1,len(x)):
                    #      user_request_text += page.searchFor(x[i])
                    #      print()
                    for i in range(len(x)):
                        user_search_text = page.searchFor(x[i])

                        text_instances = user_search_text

                        ### HIGHLIGHT
                        # if(text_instances):
                        for inst in text_instances:
                            highlight = page.addHighlightAnnot(inst)
                            out = "output" + str(i + 1)
                            # doc.save(out + ".pdf", garbage=4, deflate=True, clean=True)
                            # os.startfile(out + ".pdf")
                            # j = i

                            # spf()
                            if (instnce == 0): arr1 = i
                            # if(count==len())
                            instnce = 1

                        if instnce == 1:
                            print("instance found")
                            count = count + 1
                            print(count)
                            instnce = 0
                        #print("Can I Help you with anything else ?")
                    #print("Spf called")
                    #print(arr1)
                    if(user_count==count) :
                        doc.save(out + ".pdf", garbage=4, deflate=True, clean=True)
                        spf()
                    instnce = 0


            else:
                continue
        bot_response = "searched all files for " + user_request
    elif (greeting(user_request) != None):
        bot_response = greeting(user_request)
    else:
        bot_response = response(user_request)
    speak()
    return bot_response
