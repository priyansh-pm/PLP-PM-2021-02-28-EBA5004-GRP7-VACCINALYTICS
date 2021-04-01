from flask import Flask

from fact_check import qna_response

app = Flask(__name__)


@app.route('/vaccinalytics/fact-checker')
def fact_check():
    upload_response = qna_response()
    return upload_response


if __name__ == "__main__":
    app.run()
