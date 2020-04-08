import sys
sys.path.append('../') # append repository's home directory to identify module
import skygp.gaussian_emulator as gmu
import numpy as np
import matplotlib.pyplot as plt

emulator = gmu.GaussianEmulator()
x_train = np.array([[0.0], [1.0], [2.0]])
y_train = np.array([[0.0], [1.0], [4.0]])
emulator.fit(x_train, y_train)
ax = emulator.inspect_training_xslice(0)
ax.legend()
plt.show()

