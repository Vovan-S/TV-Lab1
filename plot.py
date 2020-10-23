import matplotlib.pyplot as plt
import numpy as np

X = np.arange(10)
Y = np.sin(X/(2*np.pi))
Z = Y**2.0
plt.plot(X, Y)
plt.show()
