from DataRetriever import DataRetriever
from TextPreparer import TextPreparer
from ResultHandler import ResultHandler
from sklearn.cluster import Birch
from ClusteringResult import ClusteringResult
from WindowFormController import WindowFormController
from StrategyBirch import StrategyBirch
from StrategyDbscan import StrategyDbscan
from StrategyKmeans import StrategyKmeans
import tkinter


class ClusteringObject:
    @staticmethod
    def main(logPath: str, startRowRegExp: str, windowFormController: WindowFormController) -> ClusteringResult:
        pr = windowFormController.window
        startRowRegExp = f'({startRowRegExp})'
        textFile = DataRetriever.readFile(logPath)
        countRows = 0
        texts = DataRetriever.splitText(startRowRegExp, textFile, countRows)

        textPreparer = TextPreparer()
        leaveRowsValue = int(windowFormController.countRows.get()) if windowFormController.countRows.get() else 0
        texts = textPreparer.sliceMessages(texts, leaveRowsValue)
        train = textPreparer.prepare(
            texts,
            strip=True,
            lower=True,
            clearPunctuation=False,
            clearDigits=True,
            stopWordsEnglish=False,
            stopWordsRussian=False,
            lemmatizationEnglish=False,
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

        # clusterStrategy = StrategyBirch()
        if windowFormController.algorithmId.get() == 1:
            clusterStrategy = StrategyDbscan()
        elif windowFormController.algorithmId.get() == 2:
            clusterStrategy = StrategyBirch()
        elif windowFormController.algorithmId.get() == 3:
            nClusters = int(windowFormController.countClusters.get()) if windowFormController.countClusters.get() else 1
            clusterStrategy = StrategyKmeans(nClusters)
        else:
            clusterStrategy = StrategyBirch()

        birchPredictions = clusterStrategy.clusterize(train)
        pr.event_generate('<<clusteringFinishedEvent>>')

        birchPredictions = TextPreparer.vectorizeLabels(birchPredictions)
        [clustersItems, clustersItemsCount, clustersWords] = ResultHandler.parsePridictions(dictionary, birchPredictions, train)
        pr.event_generate('<<parsePredictionFinishedEvent>>')

        result = ClusteringResult(birchPredictions, clustersItems, clustersItemsCount, clustersWords, train, texts)

        return result
