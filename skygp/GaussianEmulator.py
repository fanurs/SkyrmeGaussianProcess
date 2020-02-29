"""A class of Gaussian process to emulate any function.

Under development: stub functions only!

Currently, this class is just a wrapper for sklearn.gaussian_process.
The purpose of this wrapper is so that alternative package for doing
Gaussian process can easily be substituted later without affect the
flow that follows after this class.

A Gaussian process can be used to emulate arbitrary function. In this
project, we are interested in emulating the relation between Skyrme
parameters and any well-behaved (continuous and smooth) physical
observables, such as n/p ratios.

"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sklearn.gaussian_process as gp

class GaussianEmulator:
    def __init__(self):
        """This creates a Gaussian emulator.

        Currently, this class is only a wrapper around
        `sklearn.GaussianProcessRegreesor`.
        """
        self.regressor = gp.GaussianProcessRegressor()
        self.x_train = None
        self.y_train = None

    def set_niterations(self, n_itr):
        """This sets the number of training iterations.

        Parameters:
            n_itr : int
                The number of training iterations.
        """
        if not isinstance(n_itr, int):
            raise TypeError('n_itr must be an integer.')

        self.regressor.n_restarts_optimizer = n_itr
        return

    def fit(self, x, y):
        """This trains the Gaussian emulator from `x` and `y`.

        Parameters:
            x : numpy array, shape (n_train, n_inputs)
                An array containing the inputs of training set.

            y : numpy array, shape (n_train, n_outputs)
                An array containing the outputs of training set.

        """
        if not isinstance(x, np.ndarray):
            raise TypeError('x must be a numpy array.')
        if not isinstance(y, np.ndarray):
            raise TypeError('y must be a numpy array.')
        if x.ndim != 2:
            raise ValueError('x must be two-dimensional.')
        if y.ndim != 2:
            raise ValueError('y must be two-dimensional.')

        self.x_train = np.copy(x)
        self.y_train = np.copy(y)
        self.regressor.fit(x, y)
        return

    def predict(self, x):
        """This returns the prediction.

        This is essentially the emulator function when training has
        been done to a satisfactory level.

        Parameters:
            x : numpy array, shape (n_train, n_inputs)
                An array containing the inputs of interest.

        Returns:
            y_pred : numpy array, shape (n_train, n_outputs)
                An array containing the outputs predicted by the emulator.
                When training is done correctly, this prediction should be
                very close to the actual outputs, and hence can be used to
                emulator the actual computation that is usually time
                consuming.

        """
        if not isinstance(x, np.ndarray):
            raise TypeError('x must be a numpy array.')

        y_pred = self.regressor.predict(x)
        return y_pred

    def inspect_training_xslice(self, ix, ax=None):
        """Plot to compare the emulator's predictions against training data.

        Parameters:
            ix : int
                The component of `self.x_train` to be plotted.

            ax : matplotlib.axes._subplots.AxesSubplot *optional*
                The matplotlib axe to be plotted.

        Returns:
            ax : matplotlib.axes._subplots.AxesSubplot

        Examples:
        ----------
        After we have trained the `GaussianEmulator`, we may inspect the 
        training results as below:

        >>> emulator = skygp.GaussianEmulator()
        >>> emulator.fit(x_train, y_train)
        >>> fig, ax = plt.subplots()
        >>> emulator.inspect_training_xslice(0, ax=ax)
        <matplotlib.axes._subplots.AxesSubplot>

        """
        if not isinstance(ix, int):
            raise TypeError('ix must be an integer.')
        if ax is not None and not isinstance(ax, mpl.axes.Axes):
            raise TypeError('ax must be a matplotlib.axes.Axes object.')

        # create ax if not being passed
        if ax is None: fig, ax = plt.subplots()
        
        # sort training data by i_slice
        argsort = np.argsort(self.x_train[:,ix])
        x_train_sorted = self.x_train[argsort]
        y_train_sorted = self.y_train[argsort]

        y_pred = self.predict(x_train_sorted)
        n_outputs = y_train_sorted.shape[1]
        for i in range(n_outputs):
            color = plt.cm.jet(1.0 * i/(n_outputs-1))
            x_slice = x_train_sorted[:, ix]
            ax.scatter(x_slice, y_train_sorted[:,i], color=color, label='y%d true' % i)
            ax.plot(x_slice, y_pred[:,i], color=color, linestyle='dashed', label='y%d pred' % i)
        return ax
