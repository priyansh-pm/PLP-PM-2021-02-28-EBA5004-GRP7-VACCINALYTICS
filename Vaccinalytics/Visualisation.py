from flask import Flask
from flask import render_template
from flask import send_file
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd

df = pd.read_csv('covidtweets.csv')
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

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('not.html')


@app.route('/visualize')
def visualize():
    plt.pie(y, labels=labelss, explode= myexplode, shadow=True)
    canvas = FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='img/png')


if __name__ == "__main__":
    app.run()
