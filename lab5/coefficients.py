from lab5util import *
from scipy.stats import multivariate_normal as mvnd


def count_coefs(gen_sel, N):
    rs = [[0, 0], [0, 0], [0, 0]]
    f = [pearson, spearman, quadrant]
    for i in range(N):
        s = gen_sel()
        for k in range(len(rs)):
            r = f[k](*s)
            rs[k][0] += r / N
            rs[k][1] += r**2 / N
    print('\tr\t\t\trs\t\t\trq')
    s1, s2, s3, s4 = 'E', 'E2', 'D', 's'
    for i in range(len(rs)):
        s1 += f'\t{rs[i][0]}'
        s2 += f'\t{rs[i][1]}'
        s3 += f'\t{rs[i][1] - rs[i][0]**2}'
        s4 += f'\t{np.sqrt(rs[i][1] - rs[i][0]**2)}'
    print('\n'.join([s1, s2, s3, s4]))


rs = [0, 0.5, 0.9]
ns = [20, 60, 100]
N = 1000

for n in ns:
    print(f'\n\n\t\tn = {n}\n')
    for r in rs:
        print(f'\nr = {r}\n')
        count_coefs(lambda: rvs2d(n, r), N)
    print(f'\nmixed\n')
    count_coefs(lambda: mixed(n), N)
