#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify, request, render_template
from flask_mongoengine import MongoEngine

# aws site-package
import logging
import boto3
from botocore.exceptions import ClientError
from lib.comprehend_detect import ComprehendDetect

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'FB',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "email": self.email}
                
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/', methods=['POST'])
def response():
    text = request.form.get('text')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    comp_detect = ComprehendDetect(boto3.client('comprehend'))
    text_languages = comp_detect.detect_languages(text)
    text_lang_code = text_languages[0]['LanguageCode']
    text_sentiment = comp_detect.detect_sentiment(text, text_lang_code )

    return json.dumps({'text': text,
                       'text_sentiment': text_sentiment
                       })

if __name__ == "__main__":
    app.run(debug=True)