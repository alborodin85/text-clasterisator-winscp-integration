from sklearn.cluster import DBSCAN
import numpy


class StrategyDbscan:
    @staticmethod
    def clusterize(train: numpy.ndarray) -> numpy.ndarray:
        eps = 0.2
        min_samples = 5
        clustering = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
        dbscanPredictions = clustering.fit_predict(train)

        return dbscanPredictions
