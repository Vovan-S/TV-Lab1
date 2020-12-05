import numpy as np
from scipy.stats import norm, chi2, t


gamma = 0.95
for sel in [norm.rvs(size=20), norm.rvs(size=100)]:
    xm = np.mean(sel)
    s = np.sqrt(np.mean(sel*sel) - xm**2)
    n = len(sel)
    print(f'\n\tРазмер: {n}\nxm = {xm},\ts = {s}')
    ct = t.ppf((1 + gamma) / 2, n - 1)
    chi_low = chi2.ppf((1 + gamma) / 2, n - 1)
    chi_high = chi2.ppf((1 - gamma) / 2, n - 1)
    print('\n\tКлассические интервальные оценки')
    print(f't = {ct}\nchi(1-a/2) = {chi_low},\tchi_(a/2) = {chi_high}')
    dx = s*ct*(n - 1)**(-0.5)
    print(f'm in ({xm-dx}; {xm+dx})')
    print(f's in ({s*(n/chi_low)**(0.5)}; {s*(n/chi_high)**(0.5)})')
    print('\n\tАсимптотические интервальные оценки')
    cu = norm.ppf((1 + gamma) / 2)
    dx = s * cu *(n**(-0.5))
    m4 = np.mean((sel - xm)**4)
    e = m4/(s**4) - 3
    U = cu*np.sqrt((e+2)/n)
    print(f'u(1-a/2) = {cu}, m4 = {m4}\ne = {e}, U = {U}')
    print(f'm in ({xm-dx}; {xm+dx})')
    print(f's in ({s*(1+U)**(-0.5)}; {s*(1-U)**(-0.5)})')
