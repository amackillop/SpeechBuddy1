from __future__ import print_function
import nltk
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# hotel_rev = ["Great place to be when you are in Bangalore", "The place was being renovated when I visited so the seating was limited", "Loved the ambience, loved the food", "The food is delicious but not over the top", "Service - Little slow, probably because too many people", "The place is not easy to locate", "Mushroom fried rice was tasty"]
# for sentence in hotel_rev:
#     print(sentence)
#     ss = sid.polarity_scores(sentence)
#     print(ss['compound'])
#     for k in ss:
#         print('{0}: {1}, '.format(k, ss[k]), end='')
#     print()

def sentimentCall(sentencesLIST):
    sentiArray = []
    #np.linspace(0, 1, len(sentencesLIST))
    #index = 0
    for sentence in sentencesLIST:
        print(sentence)
        ss = sid.polarity_scores(sentence)
        #print(ss)
        sentiArray.append(ss['compound'])
        # for k in ss:
        #     print('{0}: {1}, '.format(k, ss[k]), end='')
        # print()
    return sentiArray



# arraySS = sentimentCall(hotel_rev)
# print(arraySS)