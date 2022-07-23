import numpy
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

class ClusterVisualisator:
    @staticmethod
    def reduceDimensionality(train: numpy.ndarray, isTsne = False, isPca = False) -> list:
        reducedTsne = numpy.array([])
        reducedPca = numpy.array([])
        if isTsne:
            reducedTsne = ClusterVisualisator.__reduceDimensionalityByTsne(train)
        if isPca:
            reducedPca = ClusterVisualisator.__reduceDimensionalityByPca(train)
        return [reducedTsne, reducedPca]

    @staticmethod
    def visualizeColor(n_clusters, redusedData, dbscanPredictions):
        cmap = plt.cm.get_cmap('nipy_spectral_r', n_clusters)
        dots = plt.scatter(redusedData[:, 0], redusedData[:, 1], c=dbscanPredictions, cmap=cmap)
        colorbar = plt.colorbar(dots)
        plt.show()

    @staticmethod
    def visualizeMonocrome(reducedTsne: numpy.ndarray, reducedPca: numpy.ndarray):
        if reducedTsne.size:
            ClusterVisualisator.__buildMonocrome(reducedTsne, 'TSNE')
        if reducedPca.size:
            ClusterVisualisator.__buildMonocrome(reducedPca, 'PCA')
        return

    @staticmethod
    def __buildMonocrome(data: numpy.ndarray, title: str):
        figure, axes = plt.subplots()
        axes.scatter(data[:, 0], data[:, 1], c='black')
        axes.set_title(title)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def __reduceDimensionalityByTsne(train: numpy.ndarray) -> numpy.ndarray:
        tsne = TSNE(n_components=2, random_state=11, init='pca', learning_rate=50)
        redusedData = tsne.fit_transform(train)
        return redusedData

    @staticmethod
    def __reduceDimensionalityByPca(train: numpy.ndarray) -> numpy.ndarray:
        pca = PCA(n_components=2, random_state=11)
        pca.fit(train)
        reducedData = pca.transform(train)
        return reducedData
