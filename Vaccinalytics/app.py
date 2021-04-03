import aibot
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import os
import pandas as pd
import ast
import re
import string
from flask import send_file
import io
from fact_check import qna_response
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
df = pd.read_csv('covidtweets.csv')
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
text_file = open("templates/sentiment.html", "w")
#print(os.getcwd())
#print(result)
text_file.write(result)
text_file.close()

app = Flask(__name__)
app.static_folder = 'static'
Bootstrap(app)
#
# @app.route("/")
# def home():
#     return render_template("index.html")
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if not userText:
        try:
            userText = aibot.listen()
        except:
            return 'sorry, can you say that again or type'
    return str(aibot.qna_response(userText))


@app.route('/chat')
def chat():
    return render_template('chatindex.html')

@app.route('/sentiment')
def sentiment():
    return render_template('not.html')

@app.route('/dashboard')
def dashboard():
    return render_template('factorbust.html')

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

@app.route('/visualize')
def visualize():
    return render_template('sentiment.html')

@app.route("/fact-checker-home")
def fact():
    return render_template("tweets.html")

@app.route('/vaccinalytics/fact-checker')
def fact_check():
    upload_response = qna_response()
    return upload_response


if __name__ == "__main__":
    app.run()