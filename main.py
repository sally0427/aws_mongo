import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

from lib.comprehend_detect import ComprehendDetect

import requests
from lib.scrab import scrab_title
from lib.ws import Word_Segmentation as ws
from lib.gpt2 import gpt

def usage_demo():
    print('-'*88)
    print("Welcome to the Amazon Comprehend detection demo!")
    print('-'*88)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    comp_detect = ComprehendDetect(boto3.client('comprehend'))
    with open('detect_sample.txt', encoding='utf-8') as sample_file:
        comment_text = sample_file.read()

    demo_size = 3

    print("Sample text used for this demo:")
    print('-'*88)
    print('comment_text:', comment_text)
    print('-'*88)

    print("Detecting languages.")
    comment_languages = comp_detect.detect_languages(comment_text)
    print("comment_languages:")
    pprint( comment_languages)
    comment_lang_code = comment_languages[0]['LanguageCode']
    

    print("Detecting sentiment.")
    comment_sentiment = comp_detect.detect_sentiment(comment_text, comment_lang_code )
    print(f"Sentiment: {comment_sentiment['Sentiment']}")
    print("SentimentScore:")
    pprint(comment_sentiment['SentimentScore'])

    print("Detecting key phrases.")
    comment_phrases = comp_detect.detect_key_phrases(comment_text, comment_lang_code)
    print(f"The first {demo_size} are:")
    pprint(comment_phrases[:demo_size])

    comment_keyWords_list = []
    for item in range(demo_size):
        comment_keyWords = comment_phrases[item]
        print(comment_keyWords)
        comment_keyWords_list.append(comment_keyWords['Text'])
    print(comment_keyWords_list)

    if (comment_sentiment['Sentiment']=='NEGATIVE'):
        print('-'*88)
        print("comment sentiment is Negative!!!!!!!!!")
        print('-'*88)
        with open('detect_sample2.txt', encoding='utf-8') as sample_file2:
            article_text = sample_file2.read()

        print('-'*88)
        print('article_text:', article_text)
        print('-'*88)

        print("Detecting languages.")
        article_languages = comp_detect.detect_languages(article_text)
        print("article_languages:")
        pprint(article_languages)
        article_lang_code = article_languages[0]['LanguageCode']

        print("Detecting key phrases.")
        article_phrases = comp_detect.detect_key_phrases(article_text, article_lang_code)
        print(f"The first {demo_size} are:")
        pprint(article_phrases[:demo_size])

        article_keyWords_list = []
        for item in range(demo_size):
            article_keyWords = article_phrases[item]
            print(article_keyWords)
            article_keyWords_list.append(article_keyWords['Text'])
        print(article_keyWords_list)

        # find the same article keywords and comment keywords
        keyword = [a for a in article_keyWords_list if a in comment_keyWords_list]
        url = "https://www.setn.com/"
        if keyword:
            result = scrab_title(url, keyword[0])
            print(result)

                        # choose positive new's title
            idex = 0
            while(1):
                news = result[idex][0]
                print('-'*88)
                print('new\'s title:', news)

                print("Detecting languages.")
                news_languages = comp_detect.detect_languages(news)
                print("news_languages:")
                pprint( news_languages)
                news_lang_code = news_languages[0]['LanguageCode']
                

                print("Detecting sentiment.")
                news_sentiment = comp_detect.detect_sentiment(news, news_lang_code )
                print(f"Sentiment: {news_sentiment['Sentiment']}")
                print("SentimentScore:")
                pprint(news_sentiment['SentimentScore'])            

                if news_sentiment['Sentiment'] == "POSITIVE":
                    print(result[idex])
                    break

                idex = idex +1
                
        # didn't have the same article keywords and comment keywords
        else:
            print('-'*88)
            print("no same key word")
            print('-'*88)

            # scab article keywords
            result = scrab_title(url, article_keyWords_list[0])
            print(result[0])
            print(result[0][0])
            
            # choose positive new's title
            idex = 0
            while(1):
                news = result[idex][0]
                print('-'*88)
                print('new\'s title:', news)

                print("Detecting languages.")
                news_languages = comp_detect.detect_languages(news)
                print("news_languages:")
                pprint( news_languages)
                news_lang_code = news_languages[0]['LanguageCode']
                

                print("Detecting sentiment.")
                news_sentiment = comp_detect.detect_sentiment(news, news_lang_code )
                print(f"Sentiment: {news_sentiment['Sentiment']}")
                print("SentimentScore:")
                pprint(news_sentiment['SentimentScore'])            

                if news_sentiment['Sentiment'] == "POSITIVE":
                    print(result[idex])
                    break

                idex = idex +1

    else:
        return 0




    print("Thanks for watching!")
    print('-'*88)



    # print('-'*88)
    # print('gpt')
    # gpt(article_text)
    # print('-'*88)


if __name__ == '__main__':
    usage_demo()
