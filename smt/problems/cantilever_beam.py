"""
Author: Dr. John T. Hwang <hwangjt@umich.edu>

Cantilever beam problem from:
Liu, H., Xu, S., & Wang, X. Sampling strategies and metamodeling techniques for engineering design: comparison and application. In ASME Turbo Expo 2016: Turbomachinery Technical Conference and Exposition. American Society of Mechanical Engineers. June, 2016.
Cheng, G. H., Younis, A., Hajikolaei, K. H., and Wang, G. G. Trust Region Based Mode Pursuing Sampling Method for Global Optimization of High Dimensional Design Problems. Journal of Mechanical Design, 137(2). 2015.
"""
from __future__ import division
import numpy as np

from smt.problems.problem import Problem


class CantileverBeam(Problem):

    def _declare_options(self):
        self.options.declare('name', 'CantileverBeam', types=str)
        self.options.declare('P', 50e3, types=(int, float), desc='Tip load (50 kN)')
        self.options.declare('E', 200e9, types=(int, float), desc='Modulus of elast. (200 GPa)')
        self.options.declare('s_a', 350e6, types=(int, float), desc='Stress allowable (350 MPa)')

    def _initialize(self):
        assert self.options['ndim'] % 3 == 0, 'ndim must be divisible by 3'

        # Width b
        self.xlimits[0::3, 0] = 0.01
        self.xlimits[0::3, 1] = 0.05

        # Height h
        self.xlimits[1::3, 0] = 0.30
        self.xlimits[1::3, 1] = 0.65

        # Length l
        self.xlimits[2::3, 0] = 0.5
        self.xlimits[2::3, 1] = 1.0

    def _evaluate(self, x, kx):
        """
        Arguments
        ---------
        x : ndarray[ne, nx]
            Evaluation points.
        kx : int or None
            Index of derivative (0-based) to return values with respect to.
            None means return function value rather than derivative.

        Returns
        -------
        ndarray[ne, 1]
            Functions values if kx=None or derivative values if kx is an int.
        """
        ne, nx = x.shape

        nelem = int(self.options['ndim'] / 3)
        P = self.options['P']
        E = self.options['E']

        y = np.zeros((ne, 1))
        if kx is None:
            for ielem in range(nelem):
                b = x[:, 3*ielem + 0]
                h = x[:, 3*ielem + 1]

                y[:, 0] += 12. / b / h ** 3 * np.sum(x[:, 2::3], axis=1) ** 3
                y[:, 0] -= 12. / b / h ** 3 * np.sum(x[:, 5 + 3*ielem::3], axis=1) ** 3
        else:
            kelem = int(np.floor(kx / 3))
            if kx % 3 == 0:
                b = x[:, 3*kelem + 0]
                h = x[:, 3*kelem + 1]
                y[:, 0] += -12. / b ** 2 / h ** 3 * np.sum(x[:, 2::3], axis=1) ** 3
                y[:, 0] -= -12. / b ** 2 / h ** 3 * np.sum(x[:, 5 + 3*kelem::3], axis=1) ** 3
            elif kx % 3 == 1:
                b = x[:, 3*kelem + 0]
                h = x[:, 3*kelem + 1]
                y[:, 0] += -36. / b / h ** 4 * np.sum(x[:, 2::3], axis=1) ** 3
                y[:, 0] -= -36. / b / h ** 4 * np.sum(x[:, 5 + 3*kelem::3], axis=1) ** 3
            elif kx % 3 == 2:
                for ielem in range(nelem):
                    b = x[:, 3*ielem + 0]
                    h = x[:, 3*ielem + 1]
                    y[:, 0] += 36. / b / h ** 3 * np.sum(x[:, 2::3], axis=1) ** 2
                    if kelem > ielem:
                       y[:, 0] -= 36. / b / h ** 3 * np.sum(x[:, 5 + 3*ielem::3], axis=1) ** 2

        return y
