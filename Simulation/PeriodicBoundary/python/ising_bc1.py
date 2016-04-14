#! /usr/bin/env python3
import textwrap
import argparse
import numpy as np
import random
import math
import time

proginfo = textwrap.dedent('''\
    This python script compares the efficiencies of different schemes
    implementing the periodic boundary conditions for Ising model problem.

    Author: JQ e-mail: gohjingqiang [at] gmail.com
    Date:   29-10-2014
''')

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=proginfo)
parser.add_argument('-l', '--L', type=int, default=10,
                    help='L, the number of spin along the edges of a \
                    2D square lattice. Default (10)')
parser.add_argument('-n', '--num', type=int, default=100,
                    help='The total number of Monte Carlo sweeps. \
                    Default (100)')
args = parser.parse_args()

start = time.time()
# Initialize the system
L = args.L
print(L)
spin = np.ones((L, L))  # 2D square lattice, spin up
T = 300  # 300 K, for temperature

# Method 1, using a separate list to mark the indices.
idx = list(range(L))
idx.insert(0, L - 1)
idx.append(0)
idx = np.array(idx, dtype=int)
random.seed(10)
for k in range(args.num):
    for i in range(L):
        for j in range(L):
            # eflip, the change in the energy of system if we flip the
            # spin[i, j]. eflip depends on the configuration of 4 neighboring
            # spins. For instance, with reference to spin[i, j], we should evaluate
            # eflip based on spin[i+1, j], spin[i-1, j], spin[i, j+1], spin[i, j-1]
            eflip = 2*spin[i, j]*(
                spin[idx[i + 1 - 1], j] +  # -1 in i-dimension
                spin[idx[i + 1 + 1], j] +  # +1 in i-dimension
                spin[i, idx[j + 1 - 1]] +  # -1 in j-dimension
                spin[i, idx[j + 1 + 1]]    # +1 in j-dimension
            )
            # Metropolis algorithm
            if eflip <= 0.0:
                spin[i, j] = -1.0*spin[i, j]
            else:
                if (random.random() < math.exp(-1.0*eflip/T)):
                    spin[i, j] = -1.0*spin[i, j]

end = time.time()
print(spin)
print(end - start)
