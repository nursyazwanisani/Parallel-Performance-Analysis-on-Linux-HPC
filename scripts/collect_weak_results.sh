#!/bin/bash
# File: scripts/collect_weak_results.sh
# Purpose: Parse raw output into clean CSV

INPUT="results/weak_results.txt"
OUTPUT="results/weak_summary.csv"

echo "processors,time,nx,ny,nt" > $OUTPUT

# Extract data using awk
awk '{print $1","$2","$3","$4","$5}' $INPUT >> $OUTPUT

echo "Summary saved to $OUTPUT"
cat $OUTPUT

