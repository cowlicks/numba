from __future__ import print_function
import numba.unittest_support as unittest
import numpy as np
from numba.compiler import compile_isolated, Flags
from numba.numpy_support import from_dtype
from numba import types


def array_itemsize(a):
    return a.itemsize


def array_shape(a, i):
    return a.shape[i]


def array_strides(a, i):
    return a.strides[i]


def array_ndim(a):
    return a.ndim


def array_size(a):
    return a.size


def nested_array_itemsize(a):
    return a.f.itemsize


def nested_array_shape(a):
    return a.f.shape


def nested_array_strides(a):
    return a.f.strides


def nested_array_ndim(a):
    return a.f.ndim


def nested_array_size(a):
    return a.f.size


class TestArrayAttr(unittest.TestCase):
    def setUp(self):
        self.a = np.arange(10).reshape(2, 5)

    def get_cfunc(self, pyfunc, argspec):
        # Need to keep a reference to the compile result for the
        # wrapper function object to remain valid (!)
        self.__cres = compile_isolated(pyfunc, argspec)
        return self.__cres.entry_point

    def test_shape(self):
        pyfunc = array_shape
        cfunc = self.get_cfunc(pyfunc, (types.int32[:,:], types.int32))

        for i in range(self.a.ndim):
            self.assertEqual(pyfunc(self.a, i), cfunc(self.a, i))

    def test_strides(self):
        pyfunc = array_strides
        cfunc = self.get_cfunc(pyfunc, (types.int32[:,:], types.int32))

        for i in range(self.a.ndim):
            self.assertEqual(pyfunc(self.a, i), cfunc(self.a, i))

    def test_ndim(self):
        pyfunc = array_ndim
        cfunc = self.get_cfunc(pyfunc, (types.int32[:,:],))

        self.assertEqual(pyfunc(self.a), cfunc(self.a))

    def test_size(self):
        pyfunc = array_size
        cfunc = self.get_cfunc(pyfunc, (types.int32[:,:],))

        self.assertEqual(pyfunc(self.a), cfunc(self.a))

    def test_itemsize(self):
        pyfunc = array_itemsize
        cfunc = self.get_cfunc(pyfunc, (types.int32[:,:],))

        self.assertEqual(pyfunc(self.a), cfunc(self.a))


class TestNestedArrayAttr(unittest.TestCase):
    def setUp(self):
        dtype = np.dtype([('a', np.int32), ('f', np.int32, (2, 5))])
        self.a = np.recarray(1, dtype)[0]
        self.nbrecord = from_dtype(self.a.dtype)

    def get_cfunc(self, pyfunc):
        # Need to keep a reference to the compile result for the
        # wrapper function object to remain valid (!)
        self.__cres = compile_isolated(pyfunc, (self.nbrecord,))
        return self.__cres.entry_point

    def test_shape(self):
        pyfunc = nested_array_shape
        cfunc = self.get_cfunc(pyfunc)

        self.assertEqual(pyfunc(self.a), cfunc(self.a))

    def test_strides(self):
        pyfunc = nested_array_strides
        cfunc = self.get_cfunc(pyfunc)

        self.assertEqual(pyfunc(self.a), cfunc(self.a))

    def test_ndim(self):
        pyfunc = nested_array_ndim
        cfunc = self.get_cfunc(pyfunc)

        self.assertEqual(pyfunc(self.a), cfunc(self.a))

    def test_size(self):
        pyfunc = nested_array_size
        cfunc = self.get_cfunc(pyfunc)

        self.assertEqual(pyfunc(self.a), cfunc(self.a))

    def test_itemsize(self):
        pyfunc = nested_array_itemsize
        cfunc = self.get_cfunc(pyfunc)

        self.assertEqual(pyfunc(self.a), cfunc(self.a))


if __name__ == '__main__':
    unittest.main()
