from __future__ import print_function, division
import numpy as np
import unittest
import inspect

from six import iteritems
from collections import OrderedDict

from smt.problems import Carre, TensorProduct
from smt.sampling import LHS

from smt.utils.sm_test_case import SMTestCase
from smt.utils.silence import Silence

from smt import LS, PA2, KPLS
try:
    from smt import IDW, RBF, RMTS, RMTB
    compiled_available = True
except:
    compiled_available = False


print_output = False

class Test(SMTestCase):

    def setUp(self):
        ndim = 10
        nt = 500
        ne = 100

        problems = OrderedDict()
        problems['carre'] = Carre(ndim=ndim)
        problems['exp'] = TensorProduct(ndim=ndim, func='exp')
        problems['tanh'] = TensorProduct(ndim=ndim, func='tanh')
        problems['cos'] = TensorProduct(ndim=ndim, func='cos')

        sms = OrderedDict()
        sms['LS'] = LS()
        sms['PA2'] = PA2()
        sms['KRG'] = KPLS(name='KRG', n_comp=ndim, theta0=[40e-2]*ndim)
        if compiled_available:
            sms['IDW'] = IDW()
            sms['RBF'] = RBF()

        t_errors = {}
        t_errors['LS'] = 1.0
        t_errors['PA2'] = 1.0
        t_errors['KRG'] = 1e-6
        t_errors['IDW'] = 1e-15
        t_errors['RBF'] = 1e-2

        e_errors = {}
        e_errors['LS'] = 1.5
        e_errors['PA2'] = 2.0
        e_errors['KRG'] = 2.0
        e_errors['IDW'] = 1.5
        e_errors['RBF'] = 1.5

        self.nt = nt
        self.ne = ne
        self.problems = problems
        self.sms = sms
        self.t_errors = t_errors
        self.e_errors = e_errors

    def run_test(self):
        method_name = inspect.stack()[1][3]
        pname = method_name.split('_')[1]
        sname = method_name.split('_')[2]

        prob = self.problems[pname]
        sampling = LHS(xlimits=prob.xlimits)

        np.random.seed(0)
        xt = sampling(self.nt)
        yt = prob(xt)

        np.random.seed(1)
        xe = sampling(self.ne)
        ye = prob(xe)

        sm0 = self.sms[sname]

        sm = sm0.__class__()
        sm.options = sm0.options.clone()
        if sm.options.is_declared('xlimits'):
            sm.options['xlimits'] = prob.xlimits
        sm.options['print_global'] = False

        sm.training_pts = {'exact': {}}
        sm.add_training_pts('exact', xt, yt)

        with Silence():
            sm.train()

        t_error = sm.compute_rms_error()
        e_error = sm.compute_rms_error(xe, ye)

        if print_output:
            print('%8s %6s %18.9e %18.9e'
                  % (pname[:6], sname, t_error, e_error))

        self.assert_error(t_error, 0., self.t_errors[sname])
        self.assert_error(e_error, 0., self.e_errors[sname])

    # --------------------------------------------------------------------
    # Function: carre

    def test_carre_LS(self):
        self.run_test()

    def test_carre_PA2(self):
        self.run_test()

    def test_carre_KRG(self):
        self.run_test()

    @unittest.skipIf(not compiled_available, 'Compiled Fortran libraries not available')
    def test_carre_IDW(self):
        self.run_test()

    @unittest.skipIf(not compiled_available, 'Compiled Fortran libraries not available')
    def test_carre_RBF(self):
        self.run_test()

    # --------------------------------------------------------------------
    # Function: exp

    def test_exp_LS(self):
        self.run_test()

    def test_exp_PA2(self):
        self.run_test()

    def test_exp_KRG(self):
        self.run_test()

    @unittest.skipIf(not compiled_available, 'Compiled Fortran libraries not available')
    def test_exp_IDW(self):
        self.run_test()

    @unittest.skipIf(not compiled_available, 'Compiled Fortran libraries not available')
    def test_exp_RBF(self):
        self.run_test()

    # --------------------------------------------------------------------
    # Function: tanh

    def test_tanh_LS(self):
        self.run_test()

    def test_tanh_PA2(self):
        self.run_test()

    def test_tanh_KRG(self):
        self.run_test()

    @unittest.skipIf(not compiled_available, 'Compiled Fortran libraries not available')
    def test_tanh_IDW(self):
        self.run_test()

    @unittest.skipIf(not compiled_available, 'Compiled Fortran libraries not available')
    def test_tanh_RBF(self):
        self.run_test()

    # --------------------------------------------------------------------
    # Function: cos

    def test_cos_LS(self):
        self.run_test()

    def test_cos_PA2(self):
        self.run_test()

    def test_cos_KRG(self):
        self.run_test()

    @unittest.skipIf(not compiled_available, 'Compiled Fortran libraries not available')
    def test_cos_IDW(self):
        self.run_test()

    @unittest.skipIf(not compiled_available, 'Compiled Fortran libraries not available')
    def test_cos_RBF(self):
        self.run_test()


if __name__ == '__main__':
    print_output = True
    print('%6s %8s %18s %18s'
          % ('SM', 'Problem', 'Train. pt. error', 'Test pt. error'))
    unittest.main()
