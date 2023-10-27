import pandas as pd
import nltk
import string
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
import contractions
import re
import spacy
from spacy.symbols import nsubj, VERB, amod, NOUN, ADJ, ADV, AUX, acomp, neg, advmod, nsubjpass
from itertools import chain
from nltk.corpus import wordnet as wn
from difflib import get_close_matches as gcm
from textblob import TextBlob

def ratingBI(ratings):
    if len(ratings) > 0:
        ratingRatio = int(sum(ratings)/(5*len(ratings))*100)
        oneStarRatio = int(ratings.count(1)/len(ratings)*100)
        twoStarRatio = int(ratings.count(2)/len(ratings)*100)
        threeStarRatio = int(ratings.count(3)/len(ratings)*100)
        fourStarRatio = int(ratings.count(4)/len(ratings)*100)
        fiveStarRatio = int(ratings.count(5)/len(ratings)*100)
        final={"numOfReviews":len(ratings), "ratingRatio":ratingRatio, "oneStarRatio": oneStarRatio, "twoStarRatio": twoStarRatio, "threeStarRatio": threeStarRatio, "fourStarRatio": fourStarRatio, "fiveStarRatio": fiveStarRatio}
    else:
        return {"numOfReviews":len(ratings), "ratingRatio":0, "oneStarRatio": 0, "twoStarRatio": 0, "threeStarRatio": 0, "fourStarRatio": 0, "fiveStarRatio": 0}
    return final

def aspectBI(texts):
    if len(texts) > 0:
        # Text preprocessing
        newTexts = ''
        for element in texts:
            newTexts += str(element)
        # Transfer to lowercase
        newTexts = newTexts.lower()
        expanded_text = []
        # Word constractions
        for word in newTexts.split():
            expanded_text.append(contractions.fix(word))
        expanded_text = ' '.join(expanded_text)
        # Manually create stopwords and remove them from sentences
        stop = ['i','it','you','they','he','she','his','her','their','my','its']
        filter_sentence= " ".join([w for w in expanded_text.split(' ') if w not in stop])
        # Remove contents in (), [], and {}
        filter_sentence = re.sub(u"\\(.*?\\)|\\{.*?\\}|\\[.*?\\]|\\<.*?\\>","", filter_sentence)
        # Split sentences by .!?
        sentences = re.findall(r"[^.!?]+", filter_sentence)
        sentences = [x.lstrip(' ') for x in sentences]
        # Load the light language model
        nlp = spacy.load('en_core_web_sm')
        aspect = ''
        description = ''
        aspects = []
        possible_adj = []
        isPositive = 1
        for sentence in sentences:
            doc = nlp(sentence)
            descriptive_term = ''
            # Analyze 3 kinds of dependencies
            for token in doc:
                # NOUN<-(nsubj)-AUX-(acomp)->ADJ
                if token.dep == nsubj and token.head.pos == AUX and token.pos == NOUN:
                    aspect = token.text
                    if aspect == "product":
                        continue
                    for child in token.head.children:
                        if child.dep == neg:
                            isPositive = 0
                        if child.dep == acomp and child.pos == ADJ:
                            description = child.text
                            aspects.append({'aspect': aspect, 'description': description, 'positive': isPositive})
                            isPositive = 1
                            break
                # NOUN<-(nsubj)-VERB-(advmod)->ADV
                elif token.dep == nsubj or nsubjpass and token.head.pos == VERB and token.pos == NOUN:
                    aspect = token.text
                    if aspect == "product":
                        continue
                    for child in token.head.children:
                        if child.dep == neg:
                            isPositive = 0
                        if child.dep == advmod and child.pos == ADV:
                            for cd in child.children:
                                if cd.dep == neg:
                                    isPositive = 0
                                # Transfer ADV to ADJ (find synonyms in wordnet)
                                if child.text == 'well':
                                    description = 'good'
                                else:
                                    for ss in wn.synsets(child.text, pos = wn.ADV):
                                        for lemmas in ss.lemmas(): # all possible lemmas
                                            for ps in lemmas.pertainyms(): # all possible pertainyms
                                                possible_adj.append(ps.name())
                                    adv2adj = gcm(child.text,possible_adj)
                                    if len(adv2adj) == 0:
                                        break
                                    else:
                                        description = adv2adj[0]
                                    aspects.append({'aspect': aspect, 'description': description, 'positive': isPositive})
                                    isPositive = 1
                                    break
                # ADJ<-(amod)-NOUN
                elif token.dep == amod and token.head.pos == NOUN:
                    aspect = token.head.text
                    if aspect == "product":
                        continue
                    prepend = ''
                    for child in token.children:
                        if child.pos_ != ADV:
                            continue
                        prepend += child.text + ''
                    descriptive_term = prepend + token.text
                    # format
                    aspects.append({'aspect': aspect, 'description': descriptive_term, 'positive': isPositive})
        # TextBlob to get the sentiment analysis result
        for aspect in aspects:
            aspect['sentiment'] = TextBlob(aspect['description']).sentiment
        # If there is negative words in the sentence, the sentiment should be reversed
        for aspect in aspects:
            if aspect['positive'] == 0:
                aspect['description'] = 'not '+ aspect['description']
                aspect['polarity'] = aspect['sentiment'].polarity * -1
            else:
                aspect['polarity'] = aspect['sentiment'].polarity
        posFeatures = []
        negFeatures = []
        # polarity < -0.5 means negative > 0.5 means positive
        for aspect in aspects:
            if  aspect['polarity'] > 0.5:
                posFeatures.append(aspect['description'] + " " + aspect['aspect'])
            elif aspect['polarity'] < -0.5:
                negFeatures.append(aspect['description'] + " " + aspect['aspect'])
        prePos = []
        preNeg = []
        removeIndexPos = []
        removeIndexNeg = []
        for aspect in aspects:
            if  aspect['polarity'] > 0.5:
                prePos.append(aspect['aspect'])
            elif aspect['polarity'] < -0.5:
                preNeg.append(aspect['aspect'])
        # Self Check (unique aspect)
        dup1 = [i for i, x in enumerate(prePos) if i != prePos.index(x)]
        dup2 = [i for i, x in enumerate(preNeg) if i != preNeg.index(x)]
        # Cross Check (remove the aspect included in both pos and neg)
        for i1,e1 in enumerate(prePos):
            isOverlap=0
            for i2,e2 in enumerate(preNeg):
                if e1 == e2:
                    isOverlap = 1
                    removeIndexNeg.append(i2)
            if isOverlap == 1:
                removeIndexPos.append(i1)
        removeIndexPos += dup1
        removeIndexNeg += dup2
        removeIndexPos = list(set(removeIndexPos))
        removeIndexNeg = list(set(removeIndexNeg))
        removeIndexPos.sort(reverse = True)
        removeIndexNeg.sort(reverse = True)
        if len(removeIndexPos) > 0:
            for i in removeIndexPos:
                del posFeatures[i]
        if len(removeIndexNeg) > 0:
            for i in removeIndexNeg:
                del negFeatures[i]
        final = {"positive": posFeatures,"negative": negFeatures}
    else:
        final = {"positive": ['NaN'],"negative": ['NaN']}
    return final