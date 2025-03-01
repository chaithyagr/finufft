# Simple 1d1 python interface call
# Lu 02/07/20.

import time
import finufft as fp
import numpy as np

np.random.seed(42)

N = int(1e6)
M = int(1e5)
x = np.random.uniform(-np.pi, np.pi, M)
x = x.astype('float32')
c = np.random.randn(M) + 1.j * np.random.randn(M)
c = c.astype('complex64')
F = np.zeros([N], dtype=np.complex64)       # allocate F (modes out)
n_modes = np.ones([1], dtype=np.int64)
n_modes[0] = N

strt = time.time()

# plan, using proper specifier for single-precision transform
plan = fp.Plan(1,(N,),dtype='complex64')

# set pts
plan.setpts(x)

# exec
plan.execute(c,F)

# timing
print("Finished nufft in {0:.2g} seconds. Checking..."
      .format(time.time()-strt))

# check error
n = 143      # mode to check
Ftest = 0.0
# this is so slow...
for j in range(M):
    Ftest += c[j] * np.exp(n * x[j] * 1.j)
Fmax = np.max(np.abs(F))
err = np.abs((F[n + N // 2] - Ftest) / Fmax)
print("Error relative to max of F: {0:.2e}".format(err))
