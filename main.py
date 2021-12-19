import numpy as np
import mykmeanssp as km
import sys
import pandas as pd

# To use this run in the terminal: python setup.py build_ext --inplace
# And on Nova: python3.8.5 setup.py build_ext --inplace

def k_means_initialization(k, data_points):
    np.random.seed(0)
    number_of_data_points = len(data_points)
    d = len(data_points[0])
    clusters = np.zeros((k, d))
    probes = np.zeros((number_of_data_points, d))
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
                if min_val > val:
                    min_val = val
            distances[l] = min_val
        probes = distances / sum(distances)
        i += 1
        rand_index = np.random.choice(data_points.shape[0], p=probes)
        index_list.append(rand_index)
        clusters[i-1] = data_points[rand_index]
    index_list.sort()
    print(index_list)
    print(clusters)
    return clusters

def norm(vector1, vector2):
    return sum((vector1 - vector2) ** 2) ** 0.5

def validate(condition):
    if not condition:
        print('Invalid Input!')
        exit(1)

# k max_iter epsilon input1 input2
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
        
        # validate(args[-3].isdigit())
        epsilon = float(args[-3])
        validate(epsilon > 0)
        input_file1 = args[-2]
        input_file2 = args[-1]

        file1 = pd.read_csv(input_file1, header=None)
        file2 = pd.read_csv(input_file2, header=None)

        inner_file = pd.merge(left=file1,right=file2,on=0, how = 'inner')
        data_points = inner_file.drop(columns=[0],axis=1).to_numpy()

        num_rows = data_points.shape[0]
        d = data_points.shape[1]

        validate(K < num_rows)

        centroids = k_means_initialization(K,data_points)


        km.fit(K,max_iter,d,num_rows,epsilon,centroids,data_points)
    except Exception:
        print('An Error Has Occurred')
        exit(1)

