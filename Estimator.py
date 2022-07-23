from sklearn import metrics
import numpy
from cdbw import CDbw
import math


class Estimator:
    @staticmethod
    def estimateByFeatures(predictions: numpy.ndarray, train: numpy.ndarray) -> dict:
        X = train
        labels = predictions

        # noinspection PyBroadException
        try:
            silhouette = metrics.silhouette_score(X=X, labels=labels)
        except:
            silhouette = math.nan

        # noinspection PyBroadException
        try:
            cdbw = CDbw(X, labels, s=3, alg_noise='filter', metric='euclidean')
        except Exception:
            cdbw = math.nan

        medResult = {
            'silhouette': silhouette,
            'cdbw': cdbw
        }

        return medResult

    @staticmethod
    def estimateByTargets(predictions: numpy.ndarray, targets: numpy.ndarray) -> list:
        """
        :param n_clusters: число кластеров
        :param predictions: список предсказанных кластеров
        :param targets: список фактических кластеров
        :param train: numpy-массив с тренировочными данными
        :return: словарь с усредненными метриками и словарь с соотношениями кластеров predictions и targets
        """
        [predictClusters, targetClusters] = Estimator.groupLabels(predictions, targets)
        matchedClusters = Estimator.matchClusters(predictClusters, targetClusters)
        medResult = Estimator.estimateByParams(matchedClusters)

        return [medResult, matchedClusters]

    @staticmethod
    def estimateByParams(matchedClusters):
        n_clusters = len(matchedClusters)
        sumPrecision = 0
        sumRecall = 0
        sumF1 = 0
        for accItem in matchedClusters:
            sumPrecision += accItem['Precision']
            sumRecall += accItem['Recall']
            sumF1 += accItem['F1']

        medResult = {
            'Precision': sumPrecision / n_clusters,
            'Recall': sumRecall / n_clusters,
            'F1': sumF1 / n_clusters,
        }

        return medResult

    @staticmethod
    def groupLabels(predictions, targets):
        predictsUniq = list(set(predictions))
        predictClusters = [[] for i in range(len(predictsUniq))]
        for predictId in range(len(predictions)):
            predictClusters[predictions[predictId]].append(predictId)

        targetsUniq = list(set(targets))
        targetClusters = [[] for i in range(len(targetsUniq))]
        for targetId in range(len(targets)):
            targetClusters[targets[targetId]].append(targetId)

        return [predictClusters, targetClusters]

    @staticmethod
    def matchClusters(predictClusters, targetClusters):
        result = []
        for predictClaster in range(len(predictClusters)):
            predictItems = predictClusters[predictClaster]
            maxAccuracy = {
                'predict_cluster': None,
                'target_cluster': None,
                'Precision': 0,
                'Recall': 0,
                'F1': 0,
            }
            for targetCluster in range(len(targetClusters)):
                targetItems = targetClusters[targetCluster]
                TP = 0  # Истинно-положительное
                FP = 0  # Ложно-положительное
                FN = 0  # Которые не найдены
                for predictItem in predictItems:
                    if predictItem in targetItems:
                        TP += 1
                    else:
                        FP += 1
                for targetItem in targetItems:
                    if targetItem not in predictItems:
                        FN += 1

                Precision = 0
                if (TP + FP) != 0:
                    Precision = TP / (TP + FP)
                Recall = 0
                if (TP + FN) != 0:
                    Recall = TP / (TP + FN)
                F1 = 0
                if Precision != 0 or Recall != 0:
                    F1 = 2 * (Precision * Recall) / (Precision + Recall)
                if F1 > maxAccuracy['F1']:
                    maxAccuracy = {
                        'predict_cluster': predictClaster,
                        'target_cluster': targetCluster,
                        'Precision': Precision,
                        'Recall': Recall,
                        'F1': F1,
                    }
            result.append(maxAccuracy)

        return result
