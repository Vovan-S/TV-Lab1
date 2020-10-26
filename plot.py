import matplotlib.pyplot as plt
import numpy as np
from histogram import Histogram
import distributions as dst

graph_disc = 200
ns = [10, 100, 1000]
ds = [dst.Normal("Normal distribution", {'mu': 0, 's': 1}),
      dst.Cauchy("Cauchy distribution", {'mu': 0, 'lambda': 1}),
      dst.Laplas("Laplas distribution", {'mu': 0, 'lambda': 2**(-0.5)}),
      dst.Poisson("Poisson distribution", {'mu': 10}),
      dst.Uniform("Uniform distribution", {'a': -3**0.5, 'b': 3**0.5})]

for d in ds:
    for n in ns:
        data = [d.x() for i in range(n)]
        hs = Histogram(data, d.discrete())
        x = np.linspace(min(data), max(data), graph_disc)
        yf = [d.f(k) for k in x]
        yF = [d.F(k) for k in x]
        plt.subplot(2, len(ns), ns.index(n) + 1)
        plt.title(d.name + ", n = " + str(n))
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.plot(x, yf, label='theoretic')
        plt.step(hs.x, hs.y, label='got')
        plt.legend()
        plt.subplot(2, len(ns), ns.index(n) + len(ns) + 1)
        plt.xlabel('x')
        plt.ylabel('F(x)')
        plt.plot(x, yF, label='theoretic')
        plt.step(hs.x, hs.F(), label='got')
        plt.legend()
    plt.show()
