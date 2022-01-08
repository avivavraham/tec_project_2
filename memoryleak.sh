#!/bin/bash

# INSTRUCTIONS:
# You must specify when running the file the resources' paths, in order
# for the code to work correctly. For instance:
# If you wish to run this script while kmeans_pp.py is inside the directory /tmp -> /tmp/kmeans_pp.py
# and while the test_data directory (containing the input files) is inside the directory /hello -> /hello/test_data
# then, the running sequences shall be: sudo ./memoryleak.sh /tmp/kmeans_pp.py /hello/test_data

# The results of the memory scan will be outputted into the reports' directory -> leak_reports
# Each report is indexed, to the corresponding running sequence specified in the test_data/test_readme.txt file.

sudo python3 setup.py build_ext --inplace

mkdir leak_reports
curl https://svn.python.org/projects/python/trunk/Misc/valgrind-python.supp > valgrind-python.supp


test_data_dir=$2
py_file=$1

function process(){
	wait $1
	awk '/HEAP SUMMARY:/{found=1} found' /tmp/reporting.txt > "leak_reports/${2}"
	rm /tmp/reporting.txt
	echo
}


valgrind --leak-check=full --track-origins=yes --show-leak-kinds=all --log-file=/tmp/reporting.txt --tool=memcheck --suppressions=valgrind-python.supp python3 -E -tt ./$1 3 333 0 "${test_data_dir}/input_1_db_1.txt" "${test_data_dir}/input_1_db_2.txt" &
process_id=$!
process $process_id "memory_leak_report1.txt"

valgrind --leak-check=full --track-origins=yes --show-leak-kinds=all --log-file=/tmp/reporting.txt --tool=memcheck --suppressions=valgrind-python.supp python3 -E -tt ./$1 7 0 "${test_data_dir}/input_2_db_1.txt" "${test_data_dir}/input_2_db_2.txt" &
process_id=$!
process $process_id "memory_leak_report2.txt"

valgrind --leak-check=full --track-origins=yes --show-leak-kinds=all --log-file=/tmp/reporting.txt --tool=memcheck --suppressions=valgrind-python.supp python3 -E -tt ./$1 15 750 0 "${test_data_dir}/input_3_db_1.txt" "${test_data_dir}/input_3_db_2.txt" &
process_id=$!
process $process_id "memory_leak_report3.txt"
