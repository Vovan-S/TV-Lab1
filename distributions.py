from random import randrange
import math
import numpy as np
from typing import Tuple


# медиана
MU = 'mu'
# стандартное отклонение
SIGMA = 's'
# срединное отклонение
LAMBDA = 'lambda'
# нижняя граница интервала
A = 'a'
# верхняя граница интервала
B = 'b'


# стандартная случайная величина (0, 1)
def r()->float:
    return randrange(1, 1000) / 1000


# Обобщенное распределение
class AbstractDistribution:
    name: str
    parameters: dict

    def __init__(self, name: str, parameters: dict):
        self.name = name
        self.parameters = parameters

    # возвращение случайной величины в соответствии с распределением
    def x(self)->float:
        return 0

    # плотность вероятности в точке x
    def f(self, x: float)->float:
        return 0

    # фукнция распределения в точке x
    def F(self, x: float)->float:
        return 0

    # границы интервала с реалистичными значениями
    # случайной величины;
    # нужно для постройки графиков
    def interval(self)->Tuple[float, float]:
        return (0, 0)

    # является ли распределние дискретным
    def discrete(self):
        return False


# Нормальное распределние
# параметры:
#   MU - медиана
#   SIGMA - стандартное отклонение
class Normal(AbstractDistribution):
    laplas_table = np.zeros(1)
    
    def f(self, x:float)->float:
        s = self.parameters[SIGMA]
        m = self.parameters[MU]
        return math.exp(-(x - m)**2/(2*s))/(s*math.sqrt(2*math.pi))

    def x(self)->float:
        y = -6
        for i in range(12):
            y += r()
        return self.parameters[MU] + self.parameters[SIGMA] * y

    def F(self, x:float)->float:
        if self.laplas_table.shape == (1,):
            self.laplas_table = np.zeros(400)
            f = open('laplas.txt')
            i = 0
            for line in f:
                self.laplas_table[i] = float(line.split()[1])
                i += 1
            # print(self.laplas_table)
        y = (x - self.parameters[MU]) / self.parameters[SIGMA]
        # print(x, y)
        n = math.floor(abs(y * 100))
        val = 0
        if n > 399:
            val = 0.9999
        else:
            val = self.laplas_table[n]
        if y > 0:
            return 0.5 + val / 2
        else:
            return 0.5 - val / 2

    def interval(self):
        s = self.parameters[SIGMA]
        m = self.parameters[MU]
        return (m - 4*s, m + 4*s)


# Распределение Коши
# Параметры:
#   MU - медиана
#   LAMBDA - среднее отклонение
class Cauchy(AbstractDistribution):
    def f(self, x: float)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        return l / (math.pi * (l**2 + (x - m)**2))

    def F(self, x:float)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        return 0.5 + math.atan((x - m)/l)/math.pi

    def x(self)->float:
        e = 0.0001
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        while True:
            y = r()
            # чтобы не получалось чересчур больших значений тангенса
            if abs(y - 0.25) > e and abs(y - 0.75) > e:
                return m + l * math.tan(2*math.pi*y)

    def interval(self)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        rng = math.sqrt(l * (300 - l))
        return (m - rng, m + rng)


# Распределение Лапласа
# Параметры:
#   MU - медиана
#   LAMBDA - параметр масштаба
class Laplas(AbstractDistribution):
    def f(self, x:float)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        return 0.5 * l * math.exp(-l * abs(x - m))

    def F(self, x:float)->float:
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        if x < m:
            return 0.5 * math.exp(l * (x - m))
        else:
            return 1 - 0.5 * math.exp(-l * (x - m))

    def x(self):
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        return m + math.log(r() / r()) / l

    def interval(self):
        l = self.parameters[LAMBDA]
        m = self.parameters[MU]
        rng = -math.log(0.002 / l)/l
        return (m - rng, m + rng)


# Распределение Пуассона
# Параметры:
#   MU - математическое ожидание
class Poisson(AbstractDistribution):
    def f(self, x: float)->float:
        if x < 0:
            return 0
        m = self.parameters[MU]
        n = math.floor(x)
        v = math.exp(-m)
        for i in range(1, n+1):
            v *= m / i
        return v

    def F(self, x:float)->float:
        if x < 0:
            return 0
        m = self.parameters[MU]
        k = math.ceil(x)
        v = math.exp(-m)
        s = v
        for i in range(1, k):
            v *= m / i
            s += v
        return s

    def x(self)->float:
        m = self.parameters[MU]        
        p = math.exp(-m)
        r1 = r() - p
        x = 0
        while r1 > 0:
            x += 1
            p *= m / x
            r1 -= p
        return x

    def interval(self):
        return (0, self.parameters[MU]*3)

    def discrete(self):
        return True


# Равномерное распределение
# Параметры:
#   A - нижняя граница интервала
#   B - верхняя граница интервала
class Uniform(AbstractDistribution):
    def f(self, x:float)->float:
        a = self.parameters[A]
        b = self.parameters[B]
        if x < a or x > b:
            return 0
        else:
            return 1 / (b - a)

    def F(self, x:float)->float:
        a = self.parameters[A]
        b = self.parameters[B]
        if x < a:
            return 0
        elif x > b:
            return 1
        else:
            return (x - a) / (b - a)

    def x(self)->float:
        a = self.parameters[A]
        b = self.parameters[B]        
        return a + (b - a)*r()

    def interval(self):
        a = self.parameters[A]
        b = self.parameters[B]
        return (a, b)


# тесты
if __name__ == "__main__":
    dist = [Normal("Normal distribution", {MU: 2, SIGMA: 2}),
            Cauchy("Cauchy distribution", {MU: 2, LAMBDA: 2}),
            Laplas("Laplas distribution", {MU: 2, LAMBDA: 2}),
            Poisson("Poisson distribution", {MU:2}),
            Uniform("Uniform distribution", {A: 0, B: 4})]
    e = 0.01
    N = 1000000
    for d in dist:
        min_x =  10000
        max_x = -10000
        a, b = d.interval()
        x0 = a + (b - a) * 0.7
        n = 0
        s = 0
        for i in range(N):
            x = d.x()
            if x < x0:
                s += 1
            if abs(x-x0) < e / 2:
                n += 1
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        print(d.name)
        print(f"x = {x0}")
        fx = n / (N * e)
        print(f"f(x) = {d.f(x0)}, f^(x) = {fx}")
        print(f"F(x) = {d.F(x0)}, F^(x) = {s / N}")

            
