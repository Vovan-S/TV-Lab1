import matplotlib.pyplot as plt
import numpy as np
from histogram import Histogram
import distributions as dst

graph_disc = 200
ns = [10, 100, 1000]
ds = [dst.Normal("Нормальное распределение", {'mu': 0, 's': 1}),
      dst.Cauchy("Распределение Коши", {'mu': 0, 'lambda': 1}),
      dst.Laplace("Распределение Лапласа", {'mu': 0, 'lambda': 2**(-0.5)}),
      dst.Poisson("Распределение Пуассона", {'mu': 10}),
      dst.Uniform("Равномерное распределение", {'a': -3**0.5, 'b': 3**0.5})]

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
        plt.ylabel('Функция плотности')
        plt.plot(x, yf, label='ожидаемое')
        plt.step(hs.x, hs.y, label='полученное')
        plt.legend()
        plt.subplot(2, len(ns), ns.index(n) + len(ns) + 1)
        plt.xlabel('x')
        plt.ylabel('Фукнция распределения')
        plt.plot(x, yF, label='ожидаемое')
        plt.step(hs.x, hs.F(), label='полученное')
        plt.legend()
    plt.show()
