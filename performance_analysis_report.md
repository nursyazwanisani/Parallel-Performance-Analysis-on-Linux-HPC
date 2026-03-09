# Parallel Performance Analysis — Summary Report

## Objective

Measure how much faster a 2D grid smoothing program runs when we split the work across multiple processors using MPI.

## Results

**Strong Scaling** — Same problem size, more processors:

<img width="1800" height="750" alt="strong_scaling" src="https://github.com/user-attachments/assets/01b60ca5-ed34-4ab2-a93e-605f15ba46c9" />

| Processors | Time (s) | Speedup | Efficiency |
|------------|----------|---------|------------|
| 1 | 0.422 | 1.00x | 100% |
| 2 | 0.230 | 1.83x | 92% |
| 4 | 0.122 | 3.46x | 86% |

The left chart shows speedup — how many times faster the program runs as we add processors. The blue line (actual) tracks close to the red dashed line (ideal), meaning the program parallelizes well. At 4 processors, we achieve 3.46x speedup out of an ideal 4x.

The right chart shows efficiency — how well each processor is being used. At 1 processor, efficiency is 100% (no communication needed). It drops to 92% at 2 processors and 86% at 4 processors. The drop is caused by time spent exchanging boundary rows between processors instead of computing.

**Weak Scaling** — Bigger problem, more processors (each processor always handles 500 rows):

<img width="1200" height="750" alt="weak_scaling" src="https://github.com/user-attachments/assets/1d5c5e2c-b06d-4555-bd20-2350fb2506e6" />

| Processors | Total Rows (NY) | Time (s) | Efficiency |
|------------|-----------------|----------|------------|
| 1 | 500 | 0.432 | 100% |
| 2 | 1,000 | 0.445 | 97% |
| 4 | 2,000 | 0.476 | 91% |

The chart shows efficiency stays close to the ideal red dashed line (1.0) as processors increase. The green line drops only slightly from 1.0 to 0.91 at 4 processors. This means we can solve a problem 4 times larger with only a 10% increase in runtime — each processor only talks to its two direct neighbors, so communication grows slowly regardless of total processor count.

## What The Numbers Mean

**Strong scaling** answers: "Can we solve the same problem faster?" Yes — 4 processors finished the job 3.46 times faster than 1 processor. Not quite 4x faster because some time is spent on processors talking to each other (exchanging boundary rows) instead of computing.

**Weak scaling** answers: "Can we solve a bigger problem in the same time?" Almost — we gave 4 processors a problem 4 times larger, and it only took 10% longer than 1 processor on the small problem. This means 91% of each processor's time is spent doing useful work, with only 9% lost to communication.

## Why It's Not Perfect

Each processor needs to share its edge data with its neighbors at every iteration. This communication takes time. As we add more processors, there are more pairs exchanging data. However, each processor only talks to its two direct neighbors (above and below), so the communication grows slowly — which is why efficiency stays high.

## Practical Recommendation

For this type of problem, 4 processors gives the best balance between speed and efficiency. This insight applies directly to real-world HPC workloads like reservoir simulation and seismic processing in oil and gas, where choosing the right number of processors saves both compute time and cluster costs.
