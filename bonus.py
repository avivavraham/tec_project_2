from sklearn import datasets
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib import patches
from kmeans_pp import k_means_initialization

# we load the iris database and calculating for k = 1 to 10 the average dispersion
# we are using KMeans algorithm with the kmeans++ initialization algorithm that we implemented
# we are ploting all the result in a chart
if __name__ == '__main__':
    iris = datasets.load_iris()
    iris_data = iris.data

    k_array = [1,2,3,4,5,6,7,8,9,10]
    average_dispersion=[]
    for k in k_array:
        initial_centroids = k_means_initialization(k,iris_data)
        kmeans = KMeans(n_clusters=k,init=initial_centroids,random_state=0,n_init=1).fit(iris_data)
        inertia = kmeans.inertia_
        average_dispersion.append(inertia)
    average_dispersion = [average_dispersion[i]/len(iris_data) for i in range(len(average_dispersion))]

    ax = plt.gca()
    ax.cla() # clear things for fresh plot
    plt.plot(k_array, average_dispersion)
    circle = patches.Ellipse((2, 1), 1,0.5, color='b', fill=False)
    plt.title('Elbow Method')
    plt.xlabel('K')
    plt.ylabel('Average Dispersion')

    ax.add_patch(circle)

    plt.savefig("elbow.png")
    plt.show()

