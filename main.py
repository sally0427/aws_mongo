import logging
from pprint import pprint
import re
import boto3
from botocore.exceptions import ClientError

from lib.comprehend_detect import ComprehendDetect

import requests
from lib.scrab import scrab_title
from lib.ws import Word_Segmentation as ws, replace_all_blank
from lib.fbcrawl import LoginFB, GetArticleText, GetCommentText
import pandas as pd 

def usage_demo():
    LoginFB()
    GetArticleText()

    with open('./dataset/article.txt', encoding='utf-8') as sample_file:
        article_text = sample_file.read()

    article_text = replace_all_blank(article_text)
    text = []
    text.append(article_text)
    article_text = ws(text)

    with open('./dataset/article.txt', 'w', encoding='utf-8') as f:
        for list in article_text:
            for item in list:
                f.write(item)
                f.write(' ')
    with open('./dataset/article.txt', encoding='utf-8') as sample_file:
        article_text = sample_file.read()

    demo_size = 3
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    comp_detect = ComprehendDetect(boto3.client('comprehend'))
    article_languages = comp_detect.detect_languages(article_text)
    article_lang_code = article_languages[0]['LanguageCode']

    article_phrases = comp_detect.detect_key_phrases(article_text, article_lang_code)
    print(f"The first {demo_size} are:")
    pprint(article_phrases[:demo_size])

    article_keyWords_list = []
    with open('./dataset/article_keywords.txt', 'w', encoding='utf-8') as sample_file:
        for item in range(demo_size):
            article_keyWords = article_phrases[item]
            sample_file.write(article_keyWords['Text'])
            sample_file.write(' ')

    with open('./dataset/article_keywords.txt', encoding='utf-8') as sample_file:
        article_keyWords_list = sample_file.read().strip().split(" ")[:3]
    print('article_keyWords_list:', article_keyWords_list)

    comment_list = GetCommentText()
    print('comment_list:', comment_list)

    for comment_text in comment_list:
        print('-'*88)
        # 文字前處理
        comment_text = replace_all_blank(comment_text)
        text = []
        text.append(comment_text)
        comment_text = ws(text)
        for list in comment_text:
            comment_text = " ".join(list)  


        comment_languages = comp_detect.detect_languages(comment_text)
        comment_lang_code = comment_languages[0]['LanguageCode']
        comment_sentiment = comp_detect.detect_sentiment(comment_text, comment_lang_code )
        print('comment:', comment_text)

        if (comment_sentiment['Sentiment']=='POSTIVE' or comment_sentiment['Sentiment']=='NEUTRAL'):
            continue

        print("Detecting key phrases.")
        comment_phrases = comp_detect.detect_key_phrases(comment_text, comment_lang_code)

        comment_keyWords_list = []
        if len(comment_phrases)<demo_size:
            size=len(comment_phrases) 
        else: 
            size=demo_size

        for item in range(size):
            comment_keyWords = comment_phrases[item]
            comment_keyWords_list.append(comment_keyWords['Text'])
        
        print('comment_keywords:', comment_keyWords_list)        

        # find the same article keywords and comment keywords
        keyword = [a for a in article_keyWords_list if a in comment_keyWords_list]
        url = "https://www.setn.com/"
        if keyword:
            print('-'*10)
            print("have same key word")
            print('-'*10)
            news_keyWords = keyword[0]
            for idex in range(1, len(keyword)):
                news_keyWords = news_keyWords + ' ' + keyword[idex]
            try:
                path = './dataset/news_' + str(article_keyWords) + '.txt'
                file = open(path, 'r')
                print('已有相同檔案，結束爬新聞')
                continue
            except:
                print('沒有相同檔案，繼續爬新聞')
                pass
            result = scrab_title(url, news_keyWords)
            if result == 0: return 0
            # result = scrab_title(url, keyword[0])
            # print(result)

            # choose positive new's title
            idex = 0
            while(idex<2):
                news = result[idex][0]
                print('-'*10)
                print('new\'s title:', news)


                news_languages = comp_detect.detect_languages(news)
                news_lang_code = news_languages[0]['LanguageCode']
                news_sentiment = comp_detect.detect_sentiment(news, news_lang_code )           

                if news_sentiment['Sentiment'] == "POSITIVE":
                    print(result[idex])
                    path = './dataset/news_' + str(keyword[0]) + '.txt'
                    print('path = ', path)
                    with open( path, 'w', encoding='utf-8') as sample_file:
                        sample_file.write(result[idex])

                idex = idex +1
                
        # didn't have the same article keywords and comment keywords
        else:
            print('-'*10)
            print("no same key word")
            print('-'*10)

            # scab article keywords
            article_keyWords = article_keyWords_list[0]
            for idex in range(1, len(article_keyWords_list)):
                article_keyWords = article_keyWords + ' ' + article_keyWords_list[idex]
            # print('article_keyWords:', article_keyWords)

            try:
                path = './dataset/news_' + str(article_keyWords) + '.csv'
                file = open(path, 'r')
                print('已有相同檔案，結束爬新聞')
                continue
            except:
                print('沒有相同檔案，繼續爬新聞')
                pass

            result = scrab_title(url, article_keyWords)
            if result == 0: return 0
            

            # choose positive new's title
            if len(result)>30:
                news_counts = 20
            elif len(result)<=20:
                news_counts = len(result)
            idex = 0
            while(idex<news_counts):
                print('-'*10)
                news = result[idex][0]
                print('new\'s title:', news)

                news_languages = comp_detect.detect_languages(news)
                news_lang_code = news_languages[0]['LanguageCode']
                news_sentiment = comp_detect.detect_sentiment(news, news_lang_code )       

                if news_sentiment['Sentiment'] == "POSITIVE":
                    print(result[idex])
                    path = './dataset/news_' + str(article_keyWords) + '.csv'
                    df = pd.DataFrame(result[idex])
                    df = df.T
                    df.to_csv(path, mode='a', index=False, header=False, encoding='utf-8-sig') 

                idex = idex +1

if __name__ == '__main__':
    usage_demo()
