#!/bin/bash
# File: scripts/run_weak_scaling.sh
# Purpose: Automate weak scaling study

PROGRAM="src/parallel_smooth.py"				
OUTPUT="results/weak_results.txt"

# Clear previous results
> $OUTPUT				

echo "Starting Weak Scaling Study..."
echo "================================"

mpiexec -np 1 python3 $PROGRAM -nx 50 -ny 500 -nt 50 >> $OUTPUT
    echo "Done 1 processor"		
mpiexec -np 2 python3 $PROGRAM -nx 50 -ny 1000 -nt 50 >> $OUTPUT
    echo "Done 2 processor"
mpiexec -np 4 python3 $PROGRAM -nx 50 -ny 2000 -nt 50 >> $OUTPUT
    echo "Done 4 processor"
echo "All done"
cat $OUTPUT


