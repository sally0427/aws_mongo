import configparser
import logging
from pprint import pprint
import boto3
from botocore.exceptions import ClientError

from lib.comprehend_detect import ComprehendDetect
import goto
# from dominate.tags import label
from goto import with_goto
from lib.scrab import scrab_title
from lib.ws import Word_Segmentation as ws, replace_all_blank
from lib.fbcrawl import LoginFB, GetArticleText, GetCommentText
from lib.keywords_extract import jieba_keywords_extract, aws_keywords_extract
import pandas as pd

@with_goto
def usage_demo():
    print('-'*88)
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    LoginFB(config['fan_page']['name'])
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
    print('article_text:', article_text)

    demo_size = 3
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    comp_detect = ComprehendDetect(boto3.client('comprehend'))

    keywords_extract_method = config['keywords_extract_method']['name']
    if keywords_extract_method == 'jieba':
        print('Start extracting keywords by jieba.')
        article_phrases = jieba_keywords_extract(article_text)

    elif keywords_extract_method == 'aws':
        print('Start extracting keywords by aws.')
        article_phrases = aws_keywords_extract(article_text, comp_detect, demo_size)


    article_keyWords_list = []
    with open('./dataset/article_keywords.txt', encoding='utf-8') as sample_file:
        article_keyWords_list = sample_file.read().strip().split(" ")[:2]
    print('article_keyWords_list:', article_keyWords_list)

    url = "https://www.setn.com/"

    # scab article keywords
    article_keyWords = article_keyWords_list[0]
    for idex in range(1, len(article_keyWords_list)):
        article_keyWords = article_keyWords + ' ' + article_keyWords_list[idex]
    # print('article_keyWords:', article_keyWords)

    try:
        path = './dataset/news_' + str(article_keyWords) + '.csv'
        file = open(path, 'r')
        print('已有相同檔案，結束爬新聞')
        # jump to comment (not yet)
        goto.comment

    except:
        print('沒有相同檔案，繼續爬新聞')

    result = scrab_title(url, article_keyWords)
    if result == 0: return 0

    # choose positive new's title
    if len(result)>int(config['news_count']['count']):
        news_counts = int(config['news_count']['count'])
    elif len(result)<=int(config['news_count']['count']):
        news_counts = len(result)
    idex = 0
    while(idex<news_counts):
        print('-'*10)
        news = result[idex][0]
        print('new\'s title:', news)

        news_languages = comp_detect.detect_languages(news)
        news_lang_code = news_languages[0]['LanguageCode']
        news_sentiment = comp_detect.detect_sentiment(news, news_lang_code )       
        print('news_sentiment:', news_sentiment['Sentiment'] )
        if news_sentiment['Sentiment'] != "NEGATIVE":
            print('result:', result[idex])
            path = './dataset/news_' + str(article_keyWords) + '.csv'
            df = pd.DataFrame(result[idex])
            df = df.T
            df.to_csv(path, mode='a', index=False, header=False, encoding='utf-8-sig') 

        idex = idex +1

    label.comment
    comment_list = GetCommentText()
    # print('comment_list:', comment_list)

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

        if (comment_sentiment['Sentiment']=='POSITIVE' or comment_sentiment['Sentiment']=='NEUTRAL'):
            continue

        print('comment:', comment_text)
        comment = []
        path = './dataset/comments_' + str(article_keyWords) + '.csv'
        comment.append(comment_text)
        df = pd.DataFrame(comment)
        df.to_csv(path, mode='a', index=False, header=False, encoding='utf-8-sig')         



if __name__ == '__main__':
    usage_demo()
