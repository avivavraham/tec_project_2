#define PY_SSIZE_T_CLEAN
#include <Python/Python.h> //for mac
// #include <Python.h> //for linux
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int find_closets_cluster(double *data_point);

void algorithm();

void init_centroids();

void free_array_2d(double **arr, int r);

void set_equal_array_2d(double **new, double **current, int r, int c);

void zero_array_2d(double **arr, int r, int c);

void calculate_new_centroids();

double **allocate_array_2d(int r, int c);

double calculate_distance_squared(double *a, double *b);

void error_occurred(int condition);

void set_clusters();

int k, max_iter, num_rows, d = 1;
int *num_elements_in_cluster;
double **data_points, **centroids, **new_centroids, **clusters;
double epsilon;

/*
 * This actually defines the geo function using a wrapper C API function
 * The wrapping function needs a PyObject* self argument.
 * This is a requirement for all functions and methods in the C API.
 * It has input PyObject *args from Python.
 */

static PyObject* fit(PyObject *self, PyObject *args){

    PyObject *pythonObject;
    
    centroids = allocate_array_2d(k, d);
    data_points = allocate_array_2d(num_rows, d);

    /* This parses the Python arguments into a double (d)  variable named z and int (i) variable named n*/
    if(!PyArg_ParseTuple(args, "iiiidOO", &k, &max_iter,&d,&num_rows,&epsilon,&centroids,&data_points)) {
        return NULL; /* In the CPython API, a NULL value is never valid for a
                        PyObject* so it is used to signal that an error has occurred. */
    }
    algorithm();

/* This builds the answer ("d" = Convert a C double to a Python floating point number) back into a python object */
    pythonObject =  Py_BuildValue("O", centroids); /*  Py_BuildValue(...) returns a PyObject*  */
    free_array_2d(centroids, k);

    return pythonObject;
}

/*
 * This array tells Python what methods this module has.
 * We will use it in the next structure
 */
static PyMethodDef capiMethods[] = {
    {"fit",                   /* the Python method name that will be used */
      (PyCFunction) fit, /* the C-function that implements the Python function and returns static PyObject*  */
      METH_VARARGS,           /* flags indicating parametersaccepted for this function */
      PyDoc_STR("algorithm to find the clusters")}, /*  The docstring for the function */
    {NULL, NULL, 0, NULL}     /* The last entry must be all NULL as shown to act as a
                                 sentinel. Python looks for this entry to know that all
                                 of the functions for the module have been defined. */
};


/* This initiates the module using the above definitions. */
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "mykmeanssp", /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,  /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    capiMethods /* the PyMethodDef array from before containing the methods of the extension */
};


/*
 * The PyModuleDef structure, in turn, must be passed to the interpreter in the module’s initialization function.
 * The initialization function must be named PyInit_name(), where name is the name of the module and should match
 * what we wrote in struct PyModuleDef.
 * This should be the only non-static item defined in the module file
 */
PyMODINIT_FUNC 
PyInit_mykmeanssp(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}

/// finish c-api 

void error_occurred(int condition) {
    if (condition == 1) {
        printf("An Error Has Occurred\n");
        exit(1);
    }
}

/*
the function gets data points and calculates the closest cluster
by the smallest squared distance from a centroid
it returns the index of the cluster in the array
*/

int find_closets_cluster(double *data_point) {
    double *difference, *current_mu, sum, min_sum;
    int index = 0, i;

    difference = calloc(k, sizeof(int *));
    error_occurred(difference == NULL);
    for (i = 0; i < k; i++) {
        current_mu = centroids[i];
        sum = calculate_distance_squared(current_mu, data_point);
        difference[i] = sum;
    }
    min_sum = difference[0];
    for (i = 0; i < k; i++) {
        if (difference[i] < min_sum) {
            min_sum = difference[i];
            index = i;
        }
    }
    free(difference);
    return index;
}

/*
the function iterate through all the data points and assigns each to the closest cluster
it calculates the num elements in each cluster
*/

void set_clusters() {
    int index, i, a;

    for (i = 0; i < k; i++) {
        num_elements_in_cluster[i] = 0;
    }
    for (i = 0; i < num_rows; i++) {
        index = find_closets_cluster(data_points[i]);
        for (a = 0; a < d; a++) {
            clusters[index][a] += data_points[i][a];
        }
        num_elements_in_cluster[index]++;
    }
}

/*
the function calculate the centroids by the new clusters that was already calculated
*/
void calculate_new_centroids() {
    double *cluster;
    int len_cluster, i, j;

    for (i = 0; i < k; i++) {
        cluster = clusters[i];
        len_cluster = num_elements_in_cluster[i];
        for (j = 0; j < d; j++) {
            new_centroids[i][j] = cluster[j] / len_cluster;
        }
    }
}

/*
the function calculate the squared distance of two points
*/

double calculate_distance_squared(double *a, double *b) {
    double distance = 0;
    int i = d;
    while (i--) {
        distance += pow(a[i] - b[i], 2);
    }
    return distance;
}

void algorithm() {
    int i, j;
    double *sum_diff_centroids;
    double diff, sq_diff, max;
    num_elements_in_cluster = calloc(k, sizeof(int));
    clusters = allocate_array_2d(k, d);
    new_centroids = allocate_array_2d(k, d);
    sum_diff_centroids = calloc(k, sizeof(double));
    while (max_iter > 0) {
        for (j = 0; j < k; j++) {
            sum_diff_centroids[j] = 0;
        }

        zero_array_2d(new_centroids, k, d);
        zero_array_2d(clusters, k, d);

        error_occurred(num_elements_in_cluster == NULL);

        set_clusters();
        calculate_new_centroids();

        max_iter--;
        error_occurred(sum_diff_centroids == NULL);

        for (i = 0; i < k; i++) {
            diff = calculate_distance_squared(centroids[i], new_centroids[i]);
            sq_diff = pow(diff, 0.5);
            sum_diff_centroids[i] = sq_diff;
        }
        max = sum_diff_centroids[0];
        for (i = 0; i < k; i++) {
            if (sum_diff_centroids[i] > max) {
                max = sum_diff_centroids[i];
            }
        }
        set_equal_array_2d(centroids, new_centroids, k, d);
        if (max <= epsilon) {
            max_iter = 0;
        }
    }
    free(sum_diff_centroids);
    free_array_2d(new_centroids, k);
    free_array_2d(data_points, num_rows);
    free_array_2d(clusters, k);
    free(num_elements_in_cluster);
}

double **allocate_array_2d(int r, int c) {
    double **arr;
    arr = calloc(r, sizeof(double *));
    error_occurred(arr == NULL);
    while (r--) {
        arr[r] = calloc(c, sizeof(double));
        error_occurred(arr[r] == NULL);
    }
    return arr;
}

void free_array_2d(double **arr, int r) {
    while (r--) {
        free(arr[r]);
    }
    free(arr);
}

void set_equal_array_2d(double **new, double **current, int r, int c) {
    int i, j;

    for (i = 0; i < r; i++) {
        for (j = 0; j < c; j++) {
            new[i][j] = current[i][j];
        }
    }
}

void zero_array_2d(double **arr, int r, int c) {
    int i, j;

    for (i = 0; i < r; i++) {
        for (j = 0; j < c; j++) {
            arr[i][j] = 0;
        }
    }
}