from sklearn.cluster import KMeans
import numpy

class StrategyKmeans:
    def __init__(self, countClustersValue: int):
        self.countClusters = countClustersValue

    def clusterize(self, train: numpy.ndarray) -> numpy.ndarray:
        clusteringModel = KMeans(n_clusters=self.countClusters, max_iter=300, random_state=21)
        clusteringModel.fit(train)
        kmeansPredictions = clusteringModel.predict(train)

        return kmeansPredictions
