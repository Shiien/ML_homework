from matplotlib import pyplot as plt
import os
from sklearn.datasets.samples_generator import make_blobs
from autograd.model.Cluster import AgglomerativeCluster


def create_data(centers, num=100, std=0.7):
    '''
    生成用于聚类的数据集
    :param centers: 聚类的中心点组成的数组。如果中心点是二维的，则产生的每个样本都是二维的。
    :param num: 样本数
    :param std: 每个簇中样本的标准差
    :return: 用于聚类的数据集。是一个元组，第一个元素为样本集，第二个元素为样本集的真实簇分类标记
    '''
    X, labels_true = make_blobs(n_samples=num, centers=centers, cluster_std=std)
    return X, labels_true


def plot_data(*data):
    '''
    绘制用于聚类的数据集
    :param data: 可变参数。它是一个元组。元组元素依次为：第一个元素为样本集，第二个元素为样本集的真实簇分类标记
    :return: None
    '''
    X, labels_true, labels_predict, name = data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    colors = 'rgbyckm'  # 每个簇的样本标记不同的颜色
    markers = 'o^sP*DX'
    for i in range(len(labels_true)):
        predict = labels_predict[i]
        ax.scatter(X[i, 0], X[i, 1], label="cluster %d" % labels_true[i],
                   color=colors[predict % len(colors)], marker=markers[labels_true[i] % len(markers)], alpha=0.5)

    ax.set_xlabel("X[0]")
    ax.set_ylabel("X[1]")
    ax.set_title("data")
    # plt.savefig(os.path.dirname(__file__) + '/images/' + name)
    # plt.show()


if __name__ == '__main__':
    import time

    Ac = AgglomerativeCluster()
    centers = [[1, 1, 1], [1, 3, 3], [3, 6, 5], [2, 6, 8]]  # 用于产生聚类的中心点, 聚类中心的维度代表产生样本的维度
    X, labels_true = create_data(centers, 1000, 0.5)  # 产 生用于聚类的数据集，聚类中心点的个数代表类别数
    K = []
    for name in ('ave', 'min', 'max'):
        Ac.fit(X, name)
        v = []
        for k in range(99, 0, -1):
            start = time.time()
            for _ in range(10):
                Ac.label(k)
            # plot_data(X, labels_true, Ac.label(k), name)
            end = time.time()
            v.append((end - start) / 10)
        # print("Execution Time: ", end - start)
        v.reverse()
        K.append(v)

    plt.plot(list(range(1, 100)), K[0], 'r', label='ave')
    plt.plot(list(range(1, 100)), K[1], 'b', label='min')
    plt.plot(list(range(1, 100)), K[2], 'g', label='max')
    plt.legend()
    plt.show()
