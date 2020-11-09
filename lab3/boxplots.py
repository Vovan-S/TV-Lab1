import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../lab1')

import distributions as dst

ds = dst.get_distributions()
ns = [20, 100]

for d in ds:
    plt.boxplot([dst.selection(d, n) for n in ns],
                vert=False,
                labels=ns)
    plt.title(d.name)
    plt.show()
