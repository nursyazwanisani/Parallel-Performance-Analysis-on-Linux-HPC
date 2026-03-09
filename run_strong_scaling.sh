#!/bin/bash
# File: scripts/run_strong_scaling.sh
# Purpose: Automate strong scaling study

PROGRAM="src/parallel_smooth.py"				
OUTPUT="results/strong_results.txt"

# Clear previous resultsi
> $OUTPUT				

echo "Starting Strong Scaling Study..."
echo "================================"

mpiexec -np 1 python3 $PROGRAM -nx 50 -ny 500 -nt 50 >> $OUTPUT
    echo "Done 1 processor"		
mpiexec -np 2 python3 $PROGRAM -nx 50 -ny 500 -nt 50 >> $OUTPUT
    echo "Done 2 processor"
mpiexec -np 4 python3 $PROGRAM -nx 50 -ny 500 -nt 50 >> $OUTPUT
    echo "Done 4 processor"
echo "All done"
cat $OUTPUT


