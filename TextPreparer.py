import sys

import numpy
import unicodedata
import numpy as np
import pandas
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from Synonymizer import Synonymizer
import re


class TextPreparer:

    def __init__(self):
        self.synonymizer = Synonymizer()

    @staticmethod
    def clearRearWords(train: pandas.Series, minCountRepeat=1, inAllDocument=False) -> pandas.Series:
        dictionary = {}
        arRows = []
        for i in range(train.size):
            row = train[i]
            words = re.split(r'\s', row)
            subDictionary = {}
            for j in range(len(words)):
                if inAllDocument:
                    if words[j] in subDictionary:
                        continue
                if words[j] in dictionary:
                    dictionary[words[j]] += 1
                else:
                    dictionary[words[j]] = 1
                subDictionary[words[j]] = 1
            arRows.append(words)

        clearDictionary = {}
        for dictPair in dictionary.items():
            if dictPair[1] > minCountRepeat:
                clearDictionary[dictPair[0]] = dictPair[1]

        clearTrain = []
        for i in range(len(arRows)):
            row = arRows[i]
            clearRow = []
            for word in row:
                if word in clearDictionary:
                    clearRow.append(word)
            clearTrain.append(' '.join(clearRow))

        return pandas.Series(clearTrain)


    @staticmethod
    def vectorizeLabels(strLabels: list) -> np.ndarray:
        labelsUniq = list(set(strLabels))
        labelVector = []
        for labelFactId in range(len(strLabels)):
            for labelNameId in range(len(labelsUniq)):
                if strLabels[labelFactId] == labelsUniq[labelNameId]:
                    labelVector.append(labelNameId)
                    break
        labelVector = np.array(labelVector)

        return labelVector

    @staticmethod
    def tfIdf(train: pandas.Series) -> list:
        tfidf = TfidfVectorizer()
        feature_matrix = tfidf.fit_transform(train)
        vocabulary = tfidf.vocabulary_
        vocabulary = pandas.Series(vocabulary)

        return [feature_matrix.toarray(), vocabulary]

    def prepare(
            self,
            train: pandas.Series,
            strip=False,
            lower=False,
            clearEmails=False,
            clearPunctuation=False,
            clearDigits=False,
            stopWordsEnglish=False,
            stopWordsRussian=False,
            lemmatizationEnglish=False,
            stemmingEnglish=False,
            stemmingRussian=False,
            sinonymizeEnglish=False
    ) -> pandas.Series:
        punctuation = dict.fromkeys([i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P')], ' ')

        digits = dict.fromkeys(
            i for i in range(sys.maxunicode) if unicodedata.category(chr(i)) == 'Nd'
        )

        def handleString(string: str) -> str:
            if lower:
                string = string.lower()
            if clearEmails:
                string = re.sub(r'\w+@\w+(\.\w+)+', '', string)
            if clearPunctuation:
                string = string.translate(punctuation)
            if strip:
                string = string.strip()
                string = re.sub(r'\s+', ' ', string)
            if clearDigits:
                string = string.translate(digits)

            nltk.download('punkt', quiet=True)
            # string = word_tokenize(string)
            string = re.split(r'\s', string)
            string = [word for word in string if word]

            if stopWordsEnglish or stopWordsRussian:
                nltk.download('stopwords', quiet=True)
                stop_words = []
                if stopWordsEnglish:
                    stop_words.extend(stopwords.words('english'))
                if stopWordsRussian:
                    stop_words.extend(stopwords.words('russian'))
                string = [word for word in string if word not in stop_words]

            if lemmatizationEnglish:
                nltk.download('wordnet', quiet=True)
                nltk.download('omw-1.4', quiet=True)
                lemmatizer = WordNetLemmatizer()
                string = [lemmatizer.lemmatize(word, pos='v') for word in string]
            if stemmingEnglish:
                porter = PorterStemmer()
                string = [porter.stem(word) for word in string]
            if stemmingRussian:
                snowball = SnowballStemmer('russian')
                string = [snowball.stem(word) for word in string]

            if sinonymizeEnglish:
                 string = [self.synonymizer.getMainSynonym(word) for word in string]

            string = ' '.join(string)

            return string

        result = train.apply(handleString)

        return result

    @staticmethod
    def splitTrainData(itemsInButch: int, train: numpy.ndarray) -> list:
        countSamples = train.shape[0]
        countButches = countSamples // itemsInButch
        itemsInLastButch = countSamples % itemsInButch
        if itemsInLastButch:
            countButches += 1
            
        if countButches == 1 :
            itemsInButch = itemsInLastButch

        batches = []
        sampleNum = 0
        for i in range(countButches):
            batches.append([])
            for j in range(itemsInButch):
                if sampleNum < train.shape[0]:
                    batches[i].append(train[sampleNum])
                sampleNum += 1

        return batches
