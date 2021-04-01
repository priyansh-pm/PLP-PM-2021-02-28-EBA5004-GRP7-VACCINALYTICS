from flask import Flask, render_template

from fact_check import qna_response

app = Flask(__name__)


@app.route("/fact-checker-home")
def home():
    return render_template("tweets.html")

@app.route('/vaccinalytics/fact-checker')
def fact_check():
    upload_response = qna_response()
    return upload_response


if __name__ == "__main__":
    app.run()
