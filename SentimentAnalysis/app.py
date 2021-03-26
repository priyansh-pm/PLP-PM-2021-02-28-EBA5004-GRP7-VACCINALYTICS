from flask import Flask
from flask import render_template
import os
import pandas as pd
import ast
import re
import string
from flask import send_file
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
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

pos, neg, neu = 0, 0, 0
for i in range(0, len(df['Analysis'])):
    if df['Analysis'][i] == 'Negative':
        neg += 1
    elif df['Analysis'][i] == 'Positive':
        pos += 1
    else:
        neu += 1

fig, ax = plt.subplots(figsize=(6, 6))

y = pos, neg, neu
labelss = ['Positive Sentiments', 'Negative Sentiments', 'Neutral Sentiments']
myexplode = [0.5, 0, 0]

@app.route('/visualize')
def visualize():
    plt.pie(y, labels=labelss, explode= myexplode, shadow=True)
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='img/png')

app.run()
