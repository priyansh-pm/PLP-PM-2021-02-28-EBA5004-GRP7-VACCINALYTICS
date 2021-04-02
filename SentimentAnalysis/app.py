from flask import Flask
from flask import render_template
import os
import pandas as pd
import ast
import re
import string
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

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

result = '<style> .dataframe { border-collapse: collapse; margin: 25px 0; font-size: 0.9em; font-family: sans-serif; min-width: 400px;box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);} .dataframe thead tr { background-color: #009879;color: #ffffff;text-align: left;} .dataframe th, .dataframe td {padding: 12px 15px;} .dataframe tbody tr { border-bottom: 1px solid #dddddd;} .dataframe tbody tr:nth-of-type(even) { background-color: #f3f3f3;} .dataframe tbody tr:last-of-type {border-bottom: 2px solid #009879;}</style>'

result = result + df[['Tweets','Subjectivity','Analysis']].to_html()
text_file = open("templates/index.html", "w")
#print(os.getcwd())
#print(result)
text_file.write(result)
text_file.close()

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
myexplode = [0.2, 0.2, 0.2]
plt.pie(y, labels=labelss, explode= myexplode, shadow=True)
canvas = FigureCanvas(fig)
img = io.BytesIO()
fig.savefig('static/a.jpg')
img.seek(0)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('not.html')

@app.route('/second')
def second():
    return render_template('index.html')

app.run()
