import mykmeanssp as km
# To use this run in the terminal: python setup.py build_ext --inplace
# And on Nova: python3.8.5 setup.py build_ext --inplace
    
km.fit(K,max_iter,d,num_rows,epsilon,centroids,data_points)