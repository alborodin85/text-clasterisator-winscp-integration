from DataRetriever import DataRetriever
from TextPreparer import TextPreparer
from ResultHandler import ResultHandler
from sklearn.cluster import Birch
from ClusteringResult import ClusteringResult
import tkinter


class ClusteringObject:
    @staticmethod
    def main(logPath: str, startRowRegExp: str, pr: tkinter.Tk) -> ClusteringResult:
        startRowRegExp = f'({startRowRegExp})'
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

        brc = Birch(threshold=0.5, branching_factor=50, n_clusters=None, compute_labels=True)
        itemsInButch = 1000
        batches = textPreparer.splitTrainData(itemsInButch, train)
        for i in range(len(batches)):
            brc.partial_fit(batches[i])
        birchPredictions = brc.predict(train)
        pr.event_generate('<<birchClusteringFinishedEvent>>')

        birchPredictions = TextPreparer.vectorizeLabels(birchPredictions)
        [clustersItems, clustersItemsCount, clustersWords] = ResultHandler.parsePridictions(dictionary, birchPredictions, train)
        pr.event_generate('<<parsePredictionFinishedEvent>>')

        result = ClusteringResult(birchPredictions, clustersItems, clustersItemsCount, clustersWords, train, texts)

        return result
