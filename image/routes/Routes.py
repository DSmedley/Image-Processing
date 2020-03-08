from image import app
from flask import request, jsonify


def analyzedJson():
    return jsonify(none=0,
                   anger=1,
                   anticipation=2,
                   disgust=3,
                   fear=4,
                   joy=5,
                   sadness=6,
                   surprise=7,
                   trust=8,
                   neutral=0,
                   positive=1,
                   negative=2,
                   top_anger="Top anger",
                   top_anticipation="Top anticipation",
                   top_disgust="Top digust",
                   top_fear="Top fear",
                   top_joy="Top joy",
                   top_sadness="Top sadness",
                   top_surprise="Top surprise",
                   top_trust="Top trust")


def iterate(object):
    for tweets in object:
        for value in tweets.values():
            print(value)
    return analyzedJson()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Image Processing API</h1>
    <p>This is a flask api for image processing</p>'''


@app.route('/v1/analyze', methods=['POST'])
def analyze():
    request_json = request.get_json()
    return iterate(request_json)
