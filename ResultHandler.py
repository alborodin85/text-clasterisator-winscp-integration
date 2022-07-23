import numpy
import pandas


class ResultHandler:
    @staticmethod
    def parsePridictions(dictionary: pandas.Series, predictions: numpy.ndarray, train: numpy.ndarray) -> list:
        targetsUniq = list(set(predictions))
        n_clusters = len(targetsUniq)

        inverseDictionary = pandas.Series(dictionary.index.values, index=dictionary.values)

        clustersItems = [[] for i in range(n_clusters)]
        clustersWords = [set([]) for i in range(n_clusters)]

        for i in range(predictions.shape[0]):
            clustersItems[predictions[i]].append(i)
            words = filter(lambda currValue: currValue[1] > 0, enumerate(train[i]))
            for wordsPair in words:
                word = inverseDictionary[wordsPair[0]]
                clustersWords[predictions[i]].add(word)

        clustersItemsCount = list(map(len, clustersItems))

        return [clustersItems, clustersItemsCount, clustersWords]
