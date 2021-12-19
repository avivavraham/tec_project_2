import numpy as np


def k_means_initialization(k, data_points):
    np.random.seed(0)
    number_of_data_points = len(data_points)
    d = len(data_points[0])
    clusters = np.zeros((k, d))
    probes = np.zeros((number_of_data_points, d))
    distances = np.zeros(number_of_data_points)
    i = 1
    rand_index = np.random.choice(data_points.shape[0])
    clusters[0] = data_points[rand_index]
    while i < k:
        for l in range(0, number_of_data_points):
            min_val = float('inf')
            for j in range(0, i):
                val = norm(data_points[l], clusters[j])
                if min_val > val:
                    min_val = val
            distances[l] = min_val
        probes = distances / sum(distances)
        i += 1
        rand_index = np.random.choice(data_points.shape[0], p=probes)
        clusters[i-1] = data_points[rand_index]
    print(clusters)
    return clusters


def norm(vector1, vector2):
    return sum((vector1 - vector2) ** 2) ** 0.5


def algorithm(k, input_file, output_file, max_iter=200):
    epsilon = 0.001
    data_points = reading_from_file(input_file)
    centroids = init_centroids(data_points, k)
    clusters = k_means_initialization(k, data_points)
    N = len(data_points)
    while max_iter > 0 and False:  # ERROR
        for i in range(N):
            x_i = data_points[i]
            index = find_closest_cluster(x_i, centroids)
            clusters[index].append(x_i)
        new_centroids = np.array([np.sum(clusters[i], axis=0) / float(len(clusters[i])) for i in range(k)])
        max_iter -= 1
        diff_centroids = centroids - new_centroids
        diff_centroids = np.array([np.sqrt(np.sum(np.square(diff_centroids[i]))) for i in range(len(diff_centroids))])
        if np.max(diff_centroids) < epsilon:
            break
        centroids = new_centroids
    #writing_to_output_file(output_file, new_centroids)


def writing_to_output_file(output_file, centroids):
    f = open(output_file, "a")
    f.write(str(np.round(centroids, 4)))
    f.close()


def find_closest_cluster(data_point, mu_array):
    difference_array = np.array([np.sqrt(np.sum(np.square(data_point - mu_array[i]))) for i in range(len(mu_array))])
    return np.argmin(difference_array)


def reading_from_file(file):
    lines = tuple(open(file, 'r'))
    vectors = np.array([np.array(line.split(",")) for line in lines]).astype(np.float)
    return vectors


def init_centroids(vectors_array, k):
    mu_array = np.array([vectors_array[i] for i in range(k)])
    return mu_array


if __name__ == '__main__':
    algorithm(3, 'input_1.txt', 'output_check')
