#!/bin/bash
# File: scripts/collect_results.sh
# Purpose: Parse raw output into clean CSV

INPUT="results/strong_results.txt"
OUTPUT="results/strong_summary.csv"

echo "processors,time,nx,ny,nt" > $OUTPUT

# Extract data using awk
awk '{print $1","$2","$3","$4","$5}' $INPUT >> $OUTPUT

echo "Summary saved to $OUTPUT"
cat $OUTPUT

