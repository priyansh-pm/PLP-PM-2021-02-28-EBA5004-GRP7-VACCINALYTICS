from flask import Flask
from flask import render_template
import os
import pandas as pd
import ast
import re
import string

df = pd.read_csv('covidtweets.csv')
#print(df.columns)
#print(df[['Tweets','Polarity','Analysis']])

for i in range(0,len(df['Tweets'])):
    df['Tweets'][i] = df['Tweets'][i].encode('ascii', 'ignore').decode()
    df['Tweets'][i] = re.sub(r'https*\S+', ' ', df['Tweets'][i])
    df['Tweets'][i] = re.sub(r'@\S+', ' ', df['Tweets'][i])
    df['Tweets'][i] = re.sub(r'#\S+', ' ', df['Tweets'][i])
    df['Tweets'][i] = re.sub(r'\'\w+', '', df['Tweets'][i])
    df['Tweets'][i] = re.sub('[%s]' % re.escape(string.punctuation), ' ', df['Tweets'][i])
    df['Tweets'][i] = re.sub(r'\w*\d+\w*', '', df['Tweets'][i])
    df['Tweets'][i] = re.sub(r'\s{2,}', ' ', df['Tweets'][i])
result = df.to_html()

text_file = open("templates/index.html", "w")
print(os.getcwd())
text_file.write(result)
text_file.close()

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

app.run()