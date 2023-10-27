from rake_nltk import Rake
import nltk
import spacy
import pandas as pd

## Visualization libraries and word frequency analysis
# loading in all the essentials for data manipulation
import pandas as pd
import numpy as np
#load inthe NTLK stopwords to remove articles, preposition and other words that are not actionable
from nltk.corpus import stopwords
# This allows to create individual objects from a bog of words
from nltk.tokenize import word_tokenize
# Lemmatizer helps to reduce words to the base form
from nltk.stem import WordNetLemmatizer
# Ngrams allows to group words in common pairs or trigrams..etc
from nltk import ngrams
# We can use counter to count the objects
from collections import Counter
# This is our visual library
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.animation as animation

from .bi import aspectBI

matplotlib.use('agg')

## natural language analysis
import re
from itertools import islice
import contractions # fix the word like i'm to i am
import spacy
from difflib import get_close_matches as gcm
from nltk.corpus import wordnet as wn
from itertools import chain
from spacy.symbols import nsubj, VERB, amod, NOUN, ADJ, ADV, AUX, acomp, neg, advmod, nsubjpass
nlp = spacy.load('en_core_web_sm')

# read database reviews
import pymysql



r = Rake()

def rake_extract(value):
    r.extract_keywords_from_text(value)
    return r.get_ranked_phrases()[0]

def get_top_keywords(keywords):
    keyword_map = {}
    top_keywords = []

    for kw in keywords:
        if (kw in keyword_map):
            keyword_map[kw] += 1
        else:
            keyword_map[kw] = 1

    if len(keyword_map.items() > 10):
        top_keywords = sorted(keyword_map.items(), key=lambda x:x[1], reverse=True)[:10]
    else:
        top_keywords = sorted(keyword_map.items(), key=lambda x:x[1], reverse=True)
    return top_keywords


"""Create a list of common words to remove"""
stop_words=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
            "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
            "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
            "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
            "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

"""Load the pre-trained NLP model in spacy"""
nlp=spacy.load("en_core_web_sm")

"""Define a function to extract keywords"""
def get_kw(x):
    doc=nlp(x) ## Tokenize and extract grammatical components
    doc=[i.text for i in doc if i.text not in stop_words and i.pos_=="NOUN"] ## Remove common words and retain only nouns
    doc=list(map(lambda i: i.lower(),doc)) ## Normalize text to lower case
    doc=pd.Series(doc)
    doc=doc.value_counts().head().index.tolist() ## Get 5 most frequent nouns
    return doc

def col_to_string(col):
    return ' '.join(col.tolist())


""" azure text summarization"""

# This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
key = "3a6a72693f234b6e890fad8bf99ad142"
endpoint = "https://reviewsummarization.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=ta_credential)
    return text_analytics_client

# Example method for summarizing text
def sample_extractive_summarization(client, review_string):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        ExtractiveSummaryAction
    )

    document = [review_string]

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractiveSummaryAction(max_sentence_count=3)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
            return "Error"
        else:
            summary_string = " ".join([sentence.text for sentence in extract_summary_result.sentences])
            print("Summary extracted: \n{}".format(summary_string))
            return summary_string

####### Generate visualization graph

# pandas read sql
con = pymysql.connect(host='webbot.mysql.database.azure.com',
                      user='admin111', password='webBot111', database='webbot')


# Data rating info
def  getRatingStatsService(productID):
    data = pd.read_sql(
        'select * from webbot_review where product_id = '+ productID ,
        'mysql+pymysql://admin111:webBot111@webbot.mysql.database.azure.com:3306/webbot')

    title = pd.read_sql(
        'select Name from webbot_product where id = ' + productID,
        'mysql+pymysql://admin111:webBot111@webbot.mysql.database.azure.com:3306/webbot')['Name'][0]
    ratingList = list(data["rating"])
    ratingLen = len(ratingList)
    final = []
    if ratingLen > 0:
        # indices = get_indices(element, pdctIdList)
        criteria = 0
        ratingRatio = sum(ratingList)/(5*ratingLen)
        oneStarRatio = ratingList.count(1)/ratingLen
        twoStarRatio = ratingList.count(2)/ratingLen
        threeStarRatio = ratingList.count(3)/ratingLen
        fourStarRatio = ratingList.count(4)/ratingLen
        fiveStarRatio = ratingList.count(5)/ratingLen
        return {'ratingRatio':ratingRatio, 'oneStar':oneStarRatio, 'twoStar':twoStarRatio, 'threeStar':threeStarRatio, 'fourStar':fourStarRatio,'fiveStar':fiveStarRatio}
    else:
        return {'ratingRatio':float("NAN"), 'oneStar':float("NAN"), 'twoStar':float("NAN"), 'threeStar':float("NAN"), 'fourStar':float("NAN"),'fiveStar':float("NAN")}


def getFeatureVisual(productid):
    data = pd.read_sql(
        'select * from webbot_review where product_id = '+ productid ,
        'mysql+pymysql://admin111:webBot111@webbot.mysql.database.azure.com:3306/webbot')

    title = pd.read_sql(
        'select Name from webbot_product where id = ' + productid,
        'mysql+pymysql://admin111:webBot111@webbot.mysql.database.azure.com:3306/webbot')['Name'][0]
    sentences = data['text']
    result = aspectBI(sentences)

    aspect = ''
    description = ''
    aspects = []
    possible_adj = []
    isPositive = 1
    expanded_text = []
    positiveList = []
    negativeList = []
    # Step 1: join the sentences and lower the case, fix the word like i'm to i am thru contractions
    # joins all the sentenses
    sentences = " ".join(sentences)

    for word in sentences.split():
        expanded_text.append(contractions.fix(word))
    expanded_text = ' '.join(expanded_text)

    # Step 2: remove words in stop list
    new_tokens = word_tokenize(expanded_text)
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens = [t for t in new_tokens if t not in stopwords.words('english')]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    lemmatizer = WordNetLemmatizer()
    new_tokens = [lemmatizer.lemmatize(t) for t in new_tokens]

    processed_sentences = " ".join(new_tokens)

    # Step 3: remove the the word in the bracket
    processed_sentences = re.sub(
        u"\\(.*?\\)|\\{.*?\\}|\\[.*?\\]|\\<.*?\\>", "", processed_sentences)
    # split sentence by . ! ?
    processed_sentences = re.findall(r"[^.!?]+", processed_sentences)
    # remove the space in the front of the sentence
    processed_sentences = [x.lstrip(' ') for x in processed_sentences]

    for sentence in processed_sentences:
        doc = nlp(sentence)
        descriptive_term = ''
        target = ''


        for token in doc:
            if token.dep == nsubj and token.head.pos == AUX and token.pos == NOUN:
                aspect = token.text
                for child in token.head.children:
                    if child.dep == neg:
                        isPositive = 0
                    if child.dep == acomp and child.pos == ADJ:
                        description = child.text
                        aspects.append(
                            {'aspect': aspect, 'description': description, 'positive': isPositive})
                        isPositive = 1
                        break
            elif token.dep == nsubj or nsubjpass and token.head.pos == VERB and token.pos == NOUN:
                aspect = token.text
                for child in token.head.children:
                    if child.dep == neg:
                        isPositive = 0
                    if child.dep == advmod and child.pos == ADV:
                        for cd in child.children:
                            if cd.dep == neg:
                                isPositive = 0
                        if child.text == 'well':
                            description = 'good'
                        else:
                            for ss in wn.synsets(child.text, pos=wn.ADV):
                                for lemmas in ss.lemmas():  # all possible lemmas
                                    for ps in lemmas.pertainyms():  # all possible pertainyms
                                        possible_adj.append(ps.name())
                            adv2adj = gcm(child.text, possible_adj)
                            if len(adv2adj) == 0:
                                break
                            else:
                                description = adv2adj[0]
                        aspects.append(
                            {'aspect': aspect, 'description': description, 'positive': isPositive})
                        isPositive = 1
                        break
            elif token.dep == amod and token.head.pos == NOUN:
                target = token.head.text
                prepend = ''
                for child in token.children:
                    if child.pos_ != ADV:
                        continue
                    prepend += child.text + ''
                descriptive_term = prepend + token.text
                aspects.append(
                    {'aspect': target, 'description': descriptive_term, 'positive': isPositive})
    for item in aspects:
        if item['positive']:
            positiveList.append((item['description'], item['aspect']))
        else:
            negativeList.append((item['description'], item['aspect']))

    # word pair counter
    countList_pos = {}
    for word in positiveList:
        for item in data['text']:
            if word[0] and word[1] in item:
                # print(word[0], word[1])
                countList_pos[(word[0], word[1])] = countList_pos.get((word[0], word[1]), 0) + 1
    countList_neg= {}
    for word in negativeList:
        for item in data['text']:
            if word[0] and word[1] in item:
                # print(word[0], word[1])
                countList_neg[(word[0], word[1])] = countList_neg.get((word[0], word[1]), 0) + 1
    return countList_pos, countList_neg


def word_frequency(productid):
    countList_pos, countList_neg = getFeatureVisual(productid)
    # print('neg list',countList_neg)
    data = pd.read_sql(
        'select * from webbot_review where product_id = '+ productid ,
        'mysql+pymysql://admin111:webBot111@webbot.mysql.database.azure.com:3306/webbot')

    title = pd.read_sql(
        'select Name from webbot_product where id = ' + productid,
        'mysql+pymysql://admin111:webBot111@webbot.mysql.database.azure.com:3306/webbot')['Name'][0]
    sentence = data['text']
    # joins all the sentenses
    sentence = " ".join(sentence)
    # creates tokens, creates lower class, removes numbers and lemmatizes the words
    new_tokens = word_tokenize(sentence)
    new_tokens = [t.lower() for t in new_tokens]
    new_tokens = [t for t in new_tokens if t not in stopwords.words('english')]
    new_tokens = [t for t in new_tokens if t.isalpha()]
    lemmatizer = WordNetLemmatizer()
    new_tokens = [lemmatizer.lemmatize(t) for t in new_tokens]
    # counts the words, pairs and trigrams
    # print(new_tokens)
    counted_2 = Counter(ngrams(new_tokens, 2))

    # creates 3 data frames and returns thems
    word_feature_pos = pd.DataFrame(countList_pos.items(), columns=[
        'pairs', 'frequency']).sort_values(by='frequency', ascending=False).head(10)
    word_feature_neg = pd.DataFrame(countList_neg.items(), columns=[
        'pairs', 'frequency']).sort_values(by='frequency', ascending=False).head(10)
    word_pairs = pd.DataFrame(counted_2.items(), columns=[
        'pairs', 'frequency']).sort_values(by='frequency', ascending=False).head(10)

    word_feature_pos['pairs'] = word_feature_pos['pairs'].astype(str)
    word_feature_neg['pairs'] = word_feature_neg['pairs'].astype(str)
    word_pairs['pairs'] = word_pairs['pairs'].astype(str)

    dataJson = {}
    dataJson['positive'] = word_feature_pos.to_dict(orient='records')
    dataJson['negative'] = word_feature_neg.to_dict(orient='records')
    dataJson['pairs'] = word_pairs.to_dict(orient='records')

    return dataJson




