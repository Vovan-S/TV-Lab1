import matplotlib.pyplot as plt
from lab5util import *


rs = [0, 0.5, 0.9]
ns = [20, 60, 100]


for i in range(len(ns)):
    fig, ax = plt.subplots(1, len(rs) + 1)
    for j in range(len(rs)):
        a = ax[j]
        s = rvs2d(ns[i], rs[j])
        a.set_title(f'n = {ns[i]}, rho = {rs[j]}')
        a.axis('equal')
        plotEllipse(*s, a, 3)
    a = ax[len(rs)]
    s = mixed(ns[i])
    a.set_title(f'n = {ns[i]}, mixed')
    a.axis('equal')
    plotEllipse(*s, a, 3)
    plt.show()

   
