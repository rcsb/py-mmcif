#!/bin/bash

# Save test start time
START_TIME=$(date +%s)

# Execute all tests

echo 'Running Test 1 ** Results stored in ./test'
../bin/FOtest1 2>&1 | tee test1.out

echo 'Running Test 2 ** Results stored in ./test'
../bin/FOtest2 2>&1 | tee test2.out

echo 'Running Test 3 ** Results stored in ./test'
../bin/FOtest3 2>&1 | tee test3.out

echo 'Running Test 4 ** Results stored in ./test'
../bin/FOtest4 -f ADH041.cif -o Test5.ocif 2>&1 | tee test4.out

echo 'Running Test 5 ** Results stored in ./test'
../bin/FOtest5 2>&1 | tee test5.out

echo 'Running Test 6 ** Results stored in ./test'
../bin/FOtest6 2>&1 | tee test6.out

echo 'Running Test 7 ** Results stored in ./test'
../bin/FOtest7 2>&1 | tee test7.out

# Commented out, since the test does not make any sense due to improper
# input binary files.
# echo 'Running Test 8 ** Results stored in ./test'
# ../bin/FOtest8 2>&1 | tee test8.out

echo 'Running Test 9 ** Results stored in ./test'
../bin/FOtest9 2>&1 | tee test9.out

echo 'Running Test 10 ** Results stored in ./test'
../bin/FOtest10 2>&1 | tee test10.out

echo 'Running Test 11 ** Results stored in ./test'
../bin/FOtest11 2>&1 | tee test11.out

echo 'Running Test 12 ** Results stored in ./test'
../bin/FOtest12 2>&1 | tee test12.out

echo 'Running Test 13 ** Results stored in ./test'
../bin/FOtest13 2>&1 | tee test13.out

echo 'Running Test 14 ** Results stored in ./test'
../bin/FOtest14 2>&1 | tee test14.out

echo 'Running Test 15 ** Results stored in ./test'
../bin/DataChecking ADH041.cif 2>&1 | tee test15.out

# Save test end time
END_TIME=$(date +%s)

DIFF_TIME=$(( $END_TIME - $START_TIME ))

echo "Tests execution time is $DIFF_TIME seconds." > exectime.txt

echo
echo
cat exectime.txt
echo
echo
