import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

from lib.comprehend_detect import ComprehendDetect
from lib.ws import Word_Segmentation as ws
from lib.gpt2 import gpt

def usage_demo():
    print('-'*88)
    print("Welcome to the Amazon Comprehend detection demo!")
    print('-'*88)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    comp_detect = ComprehendDetect(boto3.client('comprehend'))
    with open('detect_sample.txt', encoding='utf-8') as sample_file:
        sample_text = sample_file.read()

    demo_size = 3

    print("Sample text used for this demo:")
    print('-'*88)
    print(sample_text)
    print('-'*88)

    print("Detecting languages.")
    languages = comp_detect.detect_languages(sample_text)
    pprint(languages)
    lang_code = languages[0]['LanguageCode']

    print("Detecting sentiment.")
    sentiment = comp_detect.detect_sentiment(sample_text, lang_code)
    print(f"Sentiment: {sentiment['Sentiment']}")
    print("SentimentScore:")
    pprint(sentiment['SentimentScore'])

    print("Detecting key phrases.")
    phrases = comp_detect.detect_key_phrases(sample_text, lang_code)
    print(f"The first {demo_size} are:")
    pprint(phrases[:demo_size])

    print("Thanks for watching!")
    print('-'*88)

    print('-'*88)
    print('WS')
    text = []
    text.append(sample_text)
    ws(text)
    print('-'*88)

    print('-'*88)
    print('gpt')
    gpt(sample_text)
    print('-'*88)


if __name__ == '__main__':
    usage_demo()
