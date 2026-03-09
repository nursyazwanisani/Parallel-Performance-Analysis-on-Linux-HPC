#!/usr/bin/env python3
# File: src/parallel_smooth.py

from mpi4py import MPI
import numpy as np
import argparse
from time import time

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()    # My processor ID
    size = comm.Get_size()    # Total processors

    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-nx', type=int, default=1024)
    parser.add_argument('-ny', type=int, default=4096)
    parser.add_argument('-nt', type=int, default=100)
    args = parser.parse_args()
    nx, ny, nt = args.nx, args.ny, args.nt

    # Each processor gets ny/size rows
    local_ny = ny // size

    # +2 for ghost/boundary rows
    grid = np.ones((local_ny + 2, nx), dtype='float64')
    new_grid = np.zeros_like(grid)

    # Synchronize and start timing
    comm.Barrier()
    start = time()

    for t in range(nt):
        # Exchange boundaries with neighbors
        if rank > 0:
            comm.Send(grid[1,:], dest=rank-1, tag=0)
            comm.Recv(grid[0,:], source=rank-1, tag=1)
        if rank < size - 1:
            comm.Send(grid[-2,:], dest=rank+1, tag=1)
            comm.Recv(grid[-1,:], source=rank+1, tag=0)

        # Smoothing: average with neighbors
        for i in range(1, local_ny + 1):
            for j in range(1, nx - 1):
                new_grid[i,j] = 0.25 * (
                    grid[i-1,j] + grid[i+1,j] +
                    grid[i,j-1] + grid[i,j+1])

        grid[1:-1, 1:-1] = new_grid[1:-1, 1:-1]

    comm.Barrier()
    elapsed = time() - start

    # Only rank 0 prints results
    if rank == 0:
        print(f"{size:5d} {elapsed:.3E} {nx} {ny} {nt}")

if __name__ == '__main__':
    main()

