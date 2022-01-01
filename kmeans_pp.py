import numpy as np
import mykmeanssp as km
import sys
import pandas as pd

# To use this run in the terminal: python setup.py build_ext --inplace
# And on Nova: python3.8.5 setup.py build_ext --inplace


# this function receives k, the number of centroids needed. and data_points numpy array which holds the vectors data.
# this function returns numpy array of k centroids, chosen by the k-means++ algorithm.
def k_means_initialization(k, data_points,printIndex=False):
    np.random.seed(0)
    number_of_data_points = len(data_points)
    d = len(data_points[0])
    clusters = np.zeros((k, d))
    # probes = np.zeros((number_of_data_points, d))
    distances = np.zeros(number_of_data_points)
    i = 1
    index_list = []
    rand_index = np.random.choice(data_points.shape[0])
    index_list.append(rand_index)
    clusters[0] = data_points[rand_index]
    while i < k:
        for l in range(0, number_of_data_points):
            min_val = float('inf')
            for j in range(0, i):
                val = norm(data_points[l], clusters[j])
                if val <= min_val:
                    min_val = val
            distances[l] = min_val
        probes = distances / (sum(distances))
        i += 1
        rand_index = np.random.choice([i for i in range(number_of_data_points)], p=probes)
        index_list.append(rand_index)
        clusters[i-1] = data_points[rand_index]
    if printIndex:
        for i in range(len(index_list)):
            if i == len(index_list)-1:
                print(index_list[i])
            else:
                print(index_list[i], end=",")
    return clusters


# this function calculates the Euclid's l2 norm between two vectors
def norm(vector1, vector2):
    return sum((vector1 - vector2) ** 2)


# this function checks the condition if it is not true it will print "Invalid Input!" and exit
def validate(condition):
    if not condition:
        print('Invalid Input!')
        exit(1)


# this function gets the arguments from the user and process them to variables.
# this function will fill variables- k(the number of centroids) max_iter(the max number of any iteration)
# epsilon(the number of approximation accuracy needed) input1(data file number 1) input2(data file number 2)
# this function invokes k_means_initialization which return the k centroids.
# it integrates with the c-api, calls the fit function and then prints the centroids
# in case of an error it prints "An Error Has Occurred" and exit
if __name__ == '__main__':
    try:
        args = sys.argv[1:]

        validate(len(args) == 5 or len(args) == 4)

        validate(args[0].isdigit())
        K = int(args[0])
        validate(K > 1)

        if len(args) == 5:
            validate(args[1].isdigit())
            max_iter = int(args[1])
        else:
            max_iter = 300
        
        validate(args[-3].isdecimal)
        epsilon = float(args[-3])
        validate(epsilon >= 0)
        input_file1 = args[-2]
        input_file2 = args[-1]

        file1 = pd.read_csv(input_file1, header=None)
        file2 = pd.read_csv(input_file2, header=None)

        inner_file = pd.merge(left=file1, right=file2, on=0, how='inner')
        inner_file = inner_file.sort_values(by=0,axis=0)
        data_points = inner_file.drop(columns=[0], axis=1).to_numpy()

        num_rows = data_points.shape[0]
        d = data_points.shape[1]

        validate(K < num_rows)

        centroids = k_means_initialization(K, data_points,printIndex=True)

        centroids = km.fit(K, max_iter, d, num_rows, epsilon, centroids.tolist(), data_points.tolist())
        for i in range(K):
            for j in range(d):
                num = "%.4f"%float(centroids[i][j])
                if j == d-1:
                    print(num)
                else:
                    print(num, end=",")
        print("")
    except Exception:
        print('An Error Has Occurred')
        exit(1)
