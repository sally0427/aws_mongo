# -*- coding: utf-8 -*-
# import jieba 並使用繁中字典
import jieba.analyse

def jieba_keywords_extract(context):

    # 設定為繁中字典
    jieba.set_dictionary("./jieba/dict.txt.big")
    jieba.load_userdict('./jieba/userDict.txt')
    jieba.analyse.set_stop_words("./jieba/stop_words.txt")

    # 將context的前3個tags存檔
    # wtags = codecs.open("./dataset/article_keywords.txt", "w", encoding='UTF-8')
    with open('./dataset/article_keywords.txt', 'w', encoding='utf-8') as sample_file:
        words = jieba.analyse.extract_tags(context,3)
        sample_file.write(" ".join(words))

def aws_keywords_extract(article_text, comp_detect, demo_size):
    article_languages = comp_detect.detect_languages(article_text)
    article_lang_code = article_languages[0]['LanguageCode']

    article_phrases = comp_detect.detect_key_phrases(article_text, article_lang_code)
    
    with open('./dataset/article_keywords.txt', 'w', encoding='utf-8') as sample_file:
        for item in range(demo_size):
            article_keyWords = article_phrases[item]
            sample_file.write(article_keyWords['Text'])
            sample_file.write(' ')