from sklearn.cluster import Birch
from TextPreparer import TextPreparer
import numpy


class StrategyBirch:
    @staticmethod
    def clusterize(train: numpy.ndarray) -> numpy.ndarray:
        textPreparer = TextPreparer()
        brc = Birch(threshold=0.5, branching_factor=50, n_clusters=None, compute_labels=True)
        itemsInButch = 1000
        batches = textPreparer.splitTrainData(itemsInButch, train)
        for i in range(len(batches)):
            brc.partial_fit(batches[i])
        birchPredictions = brc.predict(train)

        return birchPredictions
