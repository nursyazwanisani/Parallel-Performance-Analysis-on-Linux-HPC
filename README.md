
![hpc](https://github.com/user-attachments/assets/740f0a92-4cee-41e7-be18-ad20b3a5e4a2)

# Parallel Performance Analysis on Linux HPC

A hands-on scaling study analyzing parallel performance of a 2D grid smoothing operation using MPI on a Linux environment. The project covers the full HPC workflow — from environment setup, MPI programming and performance visualization — with both strong and weak scaling analyses.

---

## Motivation

This project aims to learn Linux and HPC fundamentals, and understand how parallel programs scale. Through hands-on experiments with strong and weak scaling, I want to explore how performance changes when adding more processors to a problem. More importantly, I want to understand how to optimize computing resources and reduce costs by matching the right number of processors to the problem size. When we understand how HPC works properly, we can avoid wasting resources and money on unnecessary computing power.

---

## What This Project Does

The core program performs iterative 2D grid smoothing (a stencil operation) where each cell is averaged with its four neighbors over multiple timesteps (iterations). The grid is domain-decomposed along the Y-axis across MPI ranks (processors), with ghost-row boundary exchanges between neighboring processors at each iteration.

Two scaling studies are run against this program:

**Strong scaling** — fixed problem size (e.g. 50×500 grid, 50 iterations), increasing processor count from 1 → 2 → 4. Measures how much faster the same workload completes with more resources.

**Weak scaling** — problem size grows proportionally with processor count so each rank always handles the same local workload (e.g. 500 rows per processor). Measures whether communication overhead stays manageable as the system scales.

---

## Project Structure

```
hpc-scaling-project/
├── README.md
├── src/
│   ├── test_mpi.py               # MPI installation verification
│   ├── parallel_smooth.py        # Core parallel stencil program
│   └── plot_results.py           # Performance visualization
├── scripts/
│   ├── run_strong_scaling.sh     # Automates strong scaling runs
│   ├── run_weak_scaling.sh       # Automates weak scaling runs
│   ├── collect_strong_results.sh # Parses raw output → CSV
│   └── collect_weak_results.sh   # Parses raw output → CSV
├── results/
│   ├── strong_results.txt        # Raw timing output
│   ├── weak_results.txt          # Raw timing output
│   ├── strong_summary.csv        # Parsed summary data
│   └── weak_summary.csv          # Parsed summary data
├── plots/
    ├── strong_scaling.png        # Speedup & efficiency charts
    └── weak_scaling.png          # Weak scaling charts

```

---

## How It Works

### Domain Decomposition

The 2D grid (nx columns × ny rows) is split across processors along the Y-axis. Each processor owns `ny / N` rows plus two ghost rows for boundary exchange with its neighbors:

```
Processor 0:  rows 1–500      ↔ boundary exchange with Proc 1
Processor 1:  rows 501–1,000  ↔ boundary exchange with Proc 0 & 2
Processor 2:  rows 1,001–1,500  ↔ boundary exchange with Proc 1 & 3
Processor 3:  rows 1,501–2,000 ↔ boundary exchange with Proc 2
```

At each timestep, neighboring ranks exchange their boundary rows via `MPI.Send` / `MPI.Recv`, then each rank performs the local smoothing computation independently.

### Smoothing Operation

Each interior grid point is replaced by the average of its four direct neighbors (north, south, east, west) — a classic 5-point stencil pattern used.

---

## Results

### Strong Scaling

Fixed grid of 50×500 with 50 timesteps, varying processor count:

| Processors | Time (s) | Speedup | Efficiency |
|---|---|---|---|
| 1 | 0.422 | 1.00× | 1.00 |
| 2 | 0.230 | 1.83× | 0.92 |
| 4 | 0.122 | 3.46× | 0.86 |

Near-linear speedup with 91% parallel efficiency at 4 processors, indicating low communication overhead relative to computation at this problem size.

### Weak Scaling

Each processor handles 500 rows; total problem grows with processor count:

| Processors | Grid Size (NY) | Work/Proc | Time (s) | Efficiency |
|---|---|---|---|---|
| 1 | 500   | 500 rows | 0.432  | 1.00 |
| 2 | 1,000 | 500 rows | 0.445 | ~0.97 |
| 4 | 2,000 | 500 rows | 0.476 |~0.91 |

Efficiency remains high, confirming that the boundary exchange overhead scales sub-linearly (when processors count go from 1 to 4, the overhead cost does not quadruple) with processor count for this stencil pattern.

### Key Observations

- **Strong scaling** shows diminishing returns as the communication-to-computation ratio increases with more processors on a fixed problem.
- **Weak scaling** efficiency stays near-ideal, which is expected for stencil operations where each rank only communicates with two immediate neighbors regardless of total rank count.
- The practical implication: for this problem class, scaling to 4 processors is highly efficient. Beyond that, a larger problem size would be needed to maintain favorable computation-to-communication ratios.

---

## Quick Start

### Prerequisites

- Linux environment (Ubuntu)
- Python 3.x with `numpy`, `matplotlib`
- MPI runtime (MPICH) with `mpi4py`

### Installation

```bash
# Install MPI
sudo apt update && sudo apt install mpich

# Install Python packages
pip3 install numpy matplotlib mpi4py -break-system-packages

# Verify
mpiexec --version
python3 -c "from mpi4py import MPI; print('mpi4py OK')"
```

### Run the Studies

```bash
# Strong scaling study
bash scripts/run_strong_scaling.sh

# Weak scaling study
bash scripts/run_weak_scaling.sh

# Parse results to CSV
bash scripts/collect_strong_results.sh
bash scripts/collect_weak_results.sh

# Generate performance plots
python3 src/plot_results.py
```
---

## Technologies

- **Language**: Python 3 (NumPy, matplotlib, mpi4py)
- **Parallel framework**: MPI via MPICH
- **Scripting**: Bash
- **Version control**: Git
- **Platform**: Ubuntu Linux
