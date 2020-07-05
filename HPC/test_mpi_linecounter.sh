#!/usr/bin/bash
################################
# Author: Manodeep Sinha
# Harley-Wood School, July 2020
################################

outfilebase="linecounting_results_"
correct_fname="correct_linecounts_temp_xxxxxx.csv"
for ntask in {1..8}; do
    mpirun -np $ntask python mpi_job.py
    cat "$outfilebase"*.csv | sort -k1 | diff -q "$correct_fname" -
    retVal=$?
    if [ $retVal -ne 0 ]; then
        echo "Error: For ntasks = $ntask, the output does not match correct result"
        cat "$outfilebase"*.csv | sort -k1 > "$outfilebase_combined_$ntask.csv"
        exit $retval
    else
        echo "Passed for ntask = $ntask"
        rm -f "$outfilebase"*.csv
    fi
done
