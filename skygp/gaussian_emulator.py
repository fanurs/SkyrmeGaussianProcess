"""A module of Gaussian process to emulate any function.

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
    """A class of Gaussian emulator.

    Currently, this class is just a wrapper for sklearn.gaussian_process.
    The purpose of this wrapper is so that alternative package for doing
    Gaussian process can easily be substituted later without affect the
    flow that follows after this class.
    """

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

    def fit(self, x_train, y_train):
        """This trains the Gaussian emulator from `x_train` and `y_train`.

        Parameters:
            x_train : numpy array, shape (n_train, n_inputs)
                An array containing the inputs of training set.

            y_train : numpy array, shape (n_train, n_outputs)
                An array containing the outputs of training set.

        """
        if not isinstance(x_train, np.ndarray):
            raise TypeError('x_train must be a numpy array.')
        if not isinstance(y_train, np.ndarray):
            raise TypeError('y_train must be a numpy array.')
        if x_train.ndim != 2:
            raise ValueError('x_train must be two-dimensional.')
        if y_train.ndim != 2:
            raise ValueError('y_train must be two-dimensional.')

        self.x_train = np.copy(x_train)
        self.y_train = np.copy(y_train)
        self.regressor.fit(self.x_train, self.y_train)

    def predict(self, x_test):
        """This returns the prediction.

        This is essentially the emulator function when training has
        been done to a satisfactory level.

        Parameters:
            x_test : numpy array, shape (n_train, n_inputs)
                An array containing the inputs of interest.

        Returns:
            y_pred : numpy array, shape (n_train, n_outputs)
                An array containing the outputs predicted by the emulator.
                When training is done correctly, this prediction should be
                very close to the actual outputs, and hence can be used to
                emulator the actual computation that is usually time
                consuming.

        """
        if not isinstance(x_test, np.ndarray):
            raise TypeError('x_test must be a numpy array.')

        y_pred = self.regressor.predict(x_test)
        return y_pred

    def inspect_training_xslice(self, xslice, ax=None):
        """Plot to compare the emulator's predictions against training data.

        Parameters:
            xslice : int
                The component of `self.x_train` to be plotted.

            ax : matplotlib.axes._subplots.AxesSubplot *optional*
                The matplotlib axe to be plotted.

        Returns:
            ax : matplotlib.axes._subplots.AxesSubplot

        Examples:
        ----------
        After we have trained the `GaussianEmulator`, we may inspect the
        training results as below:

        >>> import numpy as np
        >>> import gaussian_emulator as gmu
        >>> emulator = gmu.GaussianEmulator()
        >>> x_train = np.array([[0.0], [1.0]])
        >>> y_train = np.array([[0.0], [2.0]])
        >>> emulator.fit(x_train, y_train)
        >>> emulator.inspect_training_xslice(0)
        <matplotlib.axes._subplots.AxesSubplot object at 0x...>

        """
        if not isinstance(xslice, int):
            raise TypeError('xslice must be an integer.')
        if ax is not None and not isinstance(ax, mpl.axes.Axes):
            raise TypeError('ax must be a matplotlib.axes.Axes object.')

        # create ax if not being passed
        if ax is None:
            _, ax = plt.subplots()

        # sort training data by i_slice
        argsort = np.argsort(self.x_train[:, xslice])
        x_train_sorted = self.x_train[argsort]
        y_train_sorted = self.y_train[argsort]

        y_pred = self.predict(x_train_sorted)
        n_outputs = y_train_sorted.shape[1]
        for i in range(n_outputs):
            if n_outputs > 1:
                color = plt.cm.jet(1.0 * i/(n_outputs-1))
            else:
                color = plt.cm.jet(1.0)
            x_slice = x_train_sorted[:, xslice]
            ax.scatter(x_slice, y_train_sorted[:, i], color=color, label='y%d true' % i)
            ax.plot(x_slice, y_pred[:, i], color=color, linestyle='dashed', label='y%d pred' % i)
        return ax
