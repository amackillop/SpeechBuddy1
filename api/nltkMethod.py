import nltk
import re
import json
from nltk.corpus import wordnet
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')


contractions_dict =  {
"ain't": "am not", #/ are not / is not / has not / have not,
"aren't": "are not", #
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would", #he had
"he'd've": "he would have",
"he'll": "he will", #he shall
"he'll've": " he will have", #he shall have
"he's": "he is", #he has
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is", #how has / he does
"I'd": "I would", #I had
"I'd've": "I would have",
"I'll": "I shall / I will",
"I'll've": "I will have", #I shall have
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it would",#it had
"it'd've": "it would have",
"it'll": "it will", #it shall
"it'll've": "it will have", #it shall have
"it's": "it is", #it has
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would", #she shall
"she'd've": "she would have",
"she'll": "she will", #she shall
"she'll've": "she will have", #she shall have
"she's": "she is", #she is
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so is", #so as
"that'd": "that would", #that had
"that'd've": "that would have",
"that's": "that is", #that has
"there'd": "there had / there would",
"there'd've": "there would have",
"there's": "there is", # there has
"they'd": "they would",#they had
"they'd've": "they would have",
"they'll": "they will", #they shall
"they'll've": "they will have", #they shall have
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would", #we would
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will", #what shall
"what'll've": "what will have", #what shall have
"what're": "what are",
"what's": "what is", #what has
"what've": "what have",
"when's": "when is", #when has
"when've": "when have",
"where'd": "where did",
"where's": "where is", #where has
"where've": "where have",
"who'll": "who will", #who shall
"who'll've": "who will have", #who shall have
"who's": "who is", #who has
"who've": "who have",
"why's": "why is", #why has
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",#you had
"you'd've": "you would have",
"you'll": "you will", #you shall
"you'll've": "you will have",#you shall have
"you're": "you are",
"you've": "you have"
}


contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))
def expand_contractions(s, contractions_dict=contractions_dict):
     def replace(match):
         return contractions_dict[match.group(0)]
     return contractions_re.sub(replace, s)


def mostCommon(strData):
        ps = nltk.stem.PorterStemmer()
        lemmatiser = nltk.WordNetLemmatizer()
        strData = strData.lower()
        corpus = [];
        indexArray = {}
        # str=expand_contractions(str)
        stopWords = ['the', 'a', 'an', "'s", 'they', 'with', 'to', 'of', 'should', 'every']
        tokenizer = nltk.RegexpTokenizer(r"\w+[']+\w+|\w+")
        tok = tokenizer.tokenize(strData)
        # print(tok)
        filtered_tok = []
        for i, w in enumerate(tok):
                if w.find("'") > -1:
                        if contractions_dict.get(w) is None:
                                w = w[:-2]
                if w in indexArray:
                        indexArray[w] = indexArray[w] + "," + str(i)
                else:
                        indexArray[w] = str(i)
                if w not in stopWords:
                        filtered_tok.append(lemmatiser.lemmatize(w, pos="v"))

                        # print(lemmatiser.lemmatize(w,pos="v"))

        indexArray = json.dumps(indexArray)
        freq = nltk.FreqDist(filtered_tok)
#        print(freq.most_common(16).__len__())
        listSyn = {}
        for w in freq.most_common(16):
                w = str(w)
                w = w[3:w.find(",") - 1]
                listSyn[w] = synCreate(w)
        listSyn = json.dumps(listSyn)
        corpus = [indexArray, freq.most_common(16), tok, listSyn]
        return corpus



# Problems
# 1) Context homonyms eat date / go on date
# 2) Contractions he's -> he is / he has

def synCreate(strData):
        res = {}
#        strData = strData.encode('ascii')
        syns = wordnet.synsets(strData)
        print(syns)

        for i in syns:
                for j in i.lemmas():
                        if (strData != j.name()):
                                # print(i.lemmas()[0].name())
                                examples = i.examples()
                                for n in range(len(examples)):
                                        examples[n] = examples[n]
                                if res.get(j.name()) == None:
                                        res[j.name()] = i.definition(), i.examples()
                                else:
                                        res[j.name()] = [res[j.name()],
                                                                         i.definition(),
                                                                         i.examples()]
        # print(res)
        return res

mostCommon("A string of words")