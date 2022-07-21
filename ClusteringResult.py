import numpy
import pandas


class ClusteringResult:
    def __init__(self, predictions: numpy.ndarray, clustersItems: list, clustersItemsCount: list, clustersWords: list, train: numpy.ndarray, texts: pandas.Series):
        self.predictions = predictions
        self.clustersItems = clustersItems
        self.clustersItemsCount = clustersItemsCount
        self.clustersWords = clustersWords
        self.train = train
        self.texts = texts

    def printSelf(self):
        print('ClusteringResult:')
        print('clustersItemsCount:')
        print(self.clustersItemsCount)
        print('clustersWords:')
        print(self.clustersWords)
        print('clustersItems:')
        print(self.clustersItems)
