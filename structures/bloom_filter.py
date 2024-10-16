"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from structures.bit_vector import BitVector
from structures.dynamic_array import DynamicArray
from math import ceil, log
import random
from structures.util import object_to_byte_array
from structures.entry import Entry

class BloomFilter:
    """
    A BloomFilter uses a BitVector as a container. To insert a given key, we
    hash the key using a series of h unique hash functions to set h bits.
    Looking up a given key follows the same logic, but only checks if all
    bits are set or not.

    Note that a BloomFilter is considered static. It is initialized with the
    number of total keys desired (as a parameter) and will not grow. You
    must decide what this means in terms of allocating your bitvector space
    accordingly.

    You can add functions if you need to.

    *** A NOTE ON KEYS ***
    We will only ever use int or str keys.
    We will not use `None` as a key.
    You might like to look at the `object_to_byte_array` function
    stored in util.py -- This function can be used to convert a string
    or integer key into a byte array, and then you can use the byte array
    to make your own hash function (bytes are just integers in the range
    [0-255] of course).
    """

    def __init__(self, max_keys: int) -> None:
        # You should use max_keys to decide how many bits your bitvector
        # should have, and allocate it accordingly.
        self._primes = [79, 997, 2477, 7477, 47251, 444443, 999983,
                        2000003, 4000037, 8003143]
        self._data = BitVector()
        self.max_keys = max_keys # See reference [2] here - This is where the formulas came from
        # More variables here if you need, of course
        self._fp_rate = 0.1
        self._bit_array_size =int(ceil(-max_keys*log(self._fp_rate) / log(2)**2))
        self._data.allocate(self._bit_array_size)
        self._num_hashes = int(ceil(self._bit_array_size / self.max_keys * log(2)))
        self._empty = True
        self._prime = 0
        prime_index = 0
        while self._prime < self._bit_array_size:
            self._prime = self._primes[prime_index]
            prime_index += 1
        self._hash_parameters = DynamicArray()
        for i in range(self._num_hashes):
            self._hash_parameters.append(Entry(random.randint(1, self._prime-1), random.randint(0, self._prime-1))) # Entry as dumb tuple

    def __str__(self) -> str:
        """
        A helper that allows you to print a BloomFilter type
        via the str() method.
        This is not marked. <<<<
        """
        pass

    def mad_hash(self, item, n): 
        return (abs(self._hash_parameters[n].get_key() * int.from_bytes(object_to_byte_array(item), byteorder = 'big')
                     + self._hash_parameters[n].get_value()) % self._prime) % self._bit_array_size

    def insert(self, key: Any) -> None:
        """
        Insert a key into the Bloom filter.
        Time complexity for full marks: O(1)
        """
        self._empty = False
        for i in range(self._num_hashes):
            self._data.set_at(self.mad_hash(key, i))


    def contains(self, key: Any) -> bool:
        """
        Returns True if all bits associated with the h unique hash functions
        over k are set. False otherwise.
        Time complexity for full marks: O(1)
        """
        for i in range(self._num_hashes):
            if self._data.get_at(self.mad_hash(key, i)) == 0:
                return False
        return True

    def __contains__(self, key: Any) -> bool:
        """
        Same as contains, but lets us do magic like:
        `if key in my_bloom_filter:`
        Time complexity for full marks: O(1)
        """
        return self.contains(key)

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        return self._empty

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of bits) that the underlying
        BitVector can currently maintain.
        Time complexity for full marks: O(1)
        """
        return self._bit_array_size

