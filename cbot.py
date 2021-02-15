
# coding: utf-8

# In[4]:


import nltk 
import numpy as np 
import random 
import string


# In[5]:
import os
import subprocess
import pyttsx3

import pygame

import nltk
import numpy as np
import random
import string
import os

import pyttsx3


#readtxt = open('General_desc.txt', 'rb')
f=open('vaccine-facts.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.lower()
#nltk.download('punkt')
#nltk.download('wordnet')
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)


# In[6]:


sent_tokens[:10]


# In[7]:


lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens): 
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text): 
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# In[8]:


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence): 
    for word in sentence.split(): 
        if word.lower() in GREETING_INPUTS: 
            return random.choice(GREETING_RESPONSES)


# In[9]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[10]:


def response(user_response): 
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens) 
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2] 
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    
    if(req_tfidf==0): 
        robo_response=robo_response+"I am sorry! I don't understand you" 
        return robo_response
    else: 
        robo_response = robo_response+sent_tokens[idx]
        #robo_response.save('audiobk.mp3')
        return robo_response


# In[11]:

import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init() # object creation
# Speaking rate
# engine.setProperty('rate', 200) # setting up new voice rate
# engine.runAndWait()
# rate = engine.getProperty ('rate') # getting details of current speaking rate
# engine.say("Hi")
# engine.say('My current speaking rate is' + str(rate))
# engine.runAndWait()
# engine.stop()


voices = engine.getProperty('voices')

voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

# Use female voice
engine.setProperty('voice', voice_id)

#engine.runAndWait()

def listen():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    inp = r.recognize_google(audio)
    print(inp)
    return inp

def speak():
    #engine = pyttsx3.init()  # object creation
    # Speaking rate
    engine.setProperty('rate', 180)  # setting up new voice rate
    engine.runAndWait()
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    engine.say(a)
    engine.runAndWait()
    engine.stop()

def playr():
    files = ['./Generated Speech.mp3']
    pygame.init()
    pygame.mixer.init()
    stepper = 0
    inp = 1
    import time
    # file loading
    pygame.mixer.music.load(files[stepper])
    print("Playing:", files[stepper])
    pygame.mixer.music.play()
    # play and pause
    while inp != 0:
        try:
            control = listen()
            time.sleep(3)
        except:
            print("please type")
            control = input()
        if control == "pause":
            pygame.mixer.music.pause()
        elif control == "play":
            pygame.mixer.music.unpause()
        elif control == "stop":
            pygame.mixer.music.stop()
            inp = 0




# In[ ]:


flag = True 
a = "HI , I am Chinnaswamy muthuswamy venegopala iyer . How can I assist you ? . Type bye to exit "
print(a)
speak()
while(flag == True):
    try:
        user_response = listen()
    except:
        print("please type")
        user_response = input()
    user_response = user_response.lower()
    if(user_response!='bye'):
        if(user_response == 'Thank you'):
            flag=False
            print("slb bot: you are welcome ..")
        else: 
            if(greeting(user_response)!=None):
                a = greeting(user_response)
                print("slb bot: "+ a)
                speak()

            else:
                # os.startfile("101535304_AB.pdf")
                # playr()

                print("slb bot: ",end="")
                a = response(user_response)
                print(a)
                speak()
    else: 
        flag=False
        print("slb bot: Bye! take care..")


# In[2]:


# get_ipython().system('pip install pdftotext')
# import pdftotext
#
# # Load your PDF
# with open("102923814 SWTC Flow Loop - Reference Measurement Calculations - revAE.pdf", "rb") as f:
#     pdf = pdftotext.PDF(f)
#
# # Save all text to a txt file.
# with open('output.txt', 'w') as f:
#     f.write("\n\n".join(pdf))


# In[11]:




