# A source of random bits
#
# Copyright (C) 2021 Simon Dobson
#
# This file is part of epydemic, epidemic network simulations in Python.
#
# epydemic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epydemic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epydemic. If not, see <http://www.gnu.org/licenses/gpl.html>.

from typing import Optional, Iterable
import numpy


class Bitstream(object):
    '''An infinite stream of random bits. The bits are generated from a
    random number generated by the generator in `numpy` and consumed bitwise.

    :param size: (optional) size of the entropy pool in words'''

    # Singleton instance, created on demand
    default_rng: Optional['Bitstream'] = None    #: Default bit stream generator.

    @classmethod
    def init_default_rng(cl) -> 'Bitstream':
        '''Static method to return the default bitstream. This is called
        during system initialisation so that there is a generator always
        available.

        @returns: the bitstream'''
        if cl.default_rng is None:
            cl.default_rng = Bitstream()

    # Underlying types
    Dtype = numpy.int64                        #: Type for elements of the entropy pool.
    DtypeSize = 63                             #: Bits per element (excluding sign bit).

    def __init__(self, size: int =100):
        self._rng = numpy.random.default_rng()

        self._pool: List[int] = []                      # entropy pool
        self._size = size                               # size of the pool
        self._max: int = 2 ** self.DtypeSize - 1        # maximum value of an entry in the pool
        self._element: int = 0                          # current element from the pool
        self._nelement: int = 0                         # index of current element
        self._index: int = 0                            # current bit within the element
        self._mask: int = 1                             # bit-mask

        self._refill()

    def _refill(self):
        '''Re-fill the entropy pool. This creates another batch of random numbers
        to be drawn from.'''
        self._pool = self._rng.integers(self._max, size=self._size, dtype=self.Dtype)
        self._nElement = 0
        self._element = int(self._pool[0])

    def __iter__(self) -> Iterable[int]:
        '''Return an iterator of bits.

        :retruns: an iterator'''
        return self

    def __next__(self) -> int:
        '''Return a random bit.

        :returns: a random bit'''
        bit = (self._element & self._mask) >> self._index
        self._index += 1
        self._mask <<= 1
        if self._index == self.DtypeSize:
            self._nElement += 1
            if self._nElement == self._size:
                self._refill()
            else:
                self._element = int(self._pool[self._nElement])
            self._index = 0
            self._mask = 1
        return bit

    def integer(self, n : int):
        '''Return a random integer. The integer is constructed using bits
        from the generator.

        :param n: the limit
        :returns: a random integer on the range [0, n]'''
        v = 0
        m = 1
        while True:
            m <<= 1
            if m >= n:
                return v
            else:
                v <<= 1
                v += next(self)
