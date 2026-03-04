# Parallel Performance Analysis — Summary Report

**Project:** 2D Grid Smoothing with MPI on Linux HPC  
**Author:** Nursyazwani Sani  
**Platform:** Ubuntu Server (ARM64), 4 cores, 4 GB RAM | Python 3, mpi4py, MPICH

---

## Objective

Measure how much faster a 2D grid smoothing program runs when we split the work across multiple processors using MPI.

## Results

**Strong Scaling** — Same problem size, more processors:

| Processors | Time (s) | Speedup | Efficiency |
|------------|----------|---------|------------|
| 1 | 0.422 | 1.00x | 100% |
| 2 | 0.230 | 1.83x | 92% |
| 4 | 0.122 | 3.46x | 86% |

**Weak Scaling** — Bigger problem, more processors (each processor always handles 500 rows):

| Processors | Total Rows (NY) | Time (s) | Efficiency |
|------------|-----------------|----------|------------|
| 1 | 500 | 0.432 | 100% |
| 2 | 1,000 | 0.445 | 97% |
| 4 | 2,000 | 0.476 | 91% |

## What The Numbers Mean

**Strong scaling** answers: "Can we solve the same problem faster?" Yes — 4 processors finished the job 3.46 times faster than 1 processor. Not quite 4x faster because some time is spent on processors talking to each other (exchanging boundary rows) instead of computing.

**Weak scaling** answers: "Can we solve a bigger problem in the same time?" Almost — we gave 4 processors a problem 4 times larger, and it only took 10% longer than 1 processor on the small problem. This means 91% of each processor's time is spent doing useful work, with only 9% lost to communication.

## Why It's Not Perfect

Each processor needs to share its edge data with its neighbors at every iteration. This communication takes time. As we add more processors, there are more pairs exchanging data. However, each processor only talks to its two direct neighbors (above and below), so the communication grows slowly — which is why efficiency stays high.

## Practical Recommendation

For this type of problem, 4 processors gives the best balance between speed and efficiency. This insight applies directly to real-world HPC workloads like reservoir simulation and seismic processing in oil and gas, where choosing the right number of processors saves both compute time and cluster costs.
