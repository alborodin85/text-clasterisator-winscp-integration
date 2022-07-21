import importer
import pandas_options
import numpy
from Profiler import Profiler
from DataRetriever import DataRetriever
from TextPreparer import TextPreparer
from ClusterVisualisator import ClusterVisualisator
from ResultHandler import ResultHandler
from Estimator import Estimator
from sklearn.cluster import Birch
from ClusteringResult import ClusteringResult
import tkinter

class ClusteringObject:
    @staticmethod
    def main(logPath: str, startRowRegExp: str, pr: tkinter.Tk) -> ClusteringResult:

        print(logPath)
        print(startRowRegExp)

        textFile = DataRetriever.readFile(logPath)
        countRows = 0
        texts = DataRetriever.splitText(startRowRegExp, textFile, countRows)

        textPreparer = TextPreparer()
        train = textPreparer.prepare(
            texts,
            strip=True,
            lower=True,
            clearPunctuation=True,
            clearDigits=True,
            stopWordsEnglish=True,
            stopWordsRussian=False,
            lemmatizationEnglish=True,
            stemmingEnglish=False,
            stemmingRussian=False,
            sinonymizeEnglish=False,
        )
        pr.event_generate('<<textPrepareFinishedEvent>>')

        train = TextPreparer.clearRearWords(train=train, minCountRepeat=3, inAllDocument=True)
        pr.event_generate('<<textClearRearWordsFinishedEvent>>')

        features = TextPreparer.tfIdf(train)
        train = features[0]
        dictionary = features[1]
        pr.event_generate('<<tfidfFinishedEvent>>')

        # [reducedTsne, reducedPca] = ClusterVisualisator.reduceDimensionality(train, isTsne=False, isPca=True)
        # ClusterVisualisator.visualizeMonocrome(reducedTsne, reducedPca)

        brc = Birch(threshold=0.5, branching_factor=50, n_clusters=None, compute_labels=True)

        itemsInButch = 1000

        batches = textPreparer.splitTrainData(itemsInButch, train)

        for i in range(len(batches)):
            brc.partial_fit(batches[i])

        # brc.fit(train)
        birchPredictions = brc.predict(train)

        # from sklearn.cluster import DBSCAN
        # eps = 0.2
        # min_samples = 5
        # clustering = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
        # birchPredictions = clustering.fit_predict(train)


        # targetsUniq = list(set(birchPredictions))
        # n_clusters = len(targetsUniq)

        pr.event_generate('<<birchClusteringFinishedEvent>>')

        birchPredictions = TextPreparer.vectorizeLabels(birchPredictions)
        # ClusterVisualisator.visualizeColor(n_clusters, reducedPca, birchPredictions)

        [clustersItems, clustersItemsCount, clustersWords] = ResultHandler.parsePridictions(dictionary, birchPredictions, train)
        pr.event_generate('<<parsePredictionFinishedEvent>>')

        # testCluster = clustersItems[1]
        # for sampleId in testCluster:
        #     print(texts[sampleId])

        result = ClusteringResult(birchPredictions, clustersItems, clustersItemsCount, clustersWords, train, texts)

        return result
