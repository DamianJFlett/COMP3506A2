"""
Skeleton for COMP3506/7505 A2, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov

Please read the following carefully. This file is used to implement a Map
class which supports efficient insertions, accesses, and deletions of
elements.

There is an Entry type defined in entry.py which *must* be used in your
map interface. The Entry is a very simple class that stores keys and values.
The special reason we make you use Entry types is because Entry extends the
Hashable class in util.py - by extending Hashable, you must implement
and use the `get_hash()` method inside Entry if you wish to use hashing to
implement your map. We *will* be assuming Entry types are used in your Map
implementation.
Note that if you opt to not use hashing, then you can simply override the
get_hash function to return -1 for example.
"""

from typing import Any
from structures.entry import Entry
from structures.dynamic_array import DynamicArray
from structures.linked_list import DoublyLinkedList
from structures.util import object_to_byte_array

class Map:
    """
    An implementation of the Map ADT.
    The provided methods consume keys and values via the Entry type.
    """

    def __init__(self) -> None:
        """
        Construct the map.
        You are free to make any changes you find suitable in this function
        to initialise your map.
        """
        self._primes = [79, 997, 2477, 7477, 47251, 444443, 999983,
                        2000003, 4000037, 8003143]
        self._prime_index = 0
        self._arr = DynamicArray()
        self._arr.build_from_list(
            [DoublyLinkedList() for _ in range(self._primes[0])])
        self._size = 0

    def _rehash(self):
        self._prime_index += 1
        while self._arr.get_size() < self._primes[self._prime_index]:
            self._arr.append(DoublyLinkedList())

        for i in range(self._primes[self._prime_index - 1]):
            chain = self._arr[i]
            chain_cur = chain.get_head_node()
            
            while chain_cur:
                entry = chain_cur.get_data()
                new_index = self._compress(self._get_hash(entry.get_key()))
                
                if new_index != i:
                    self._arr[i].find_and_remove_element(entry)
                    self._arr[new_index].insert_to_back(entry)
                
                chain_cur = chain_cur.get_next()

    def insert(self, entry: Entry) -> Any | None:
        """
        Associate value v with key k for efficient lookups. If k already exists
        in your map, you must return the old value associated with k. Return
        None otherwise. (We will not use None as a key or a value in our tests).
        Time complexity for full marks: O(1*)
        """
        key = entry.get_key()
        if self.get_load_factor() > 1:
            self._rehash()
        chain_cur = self._arr[self._compress(self._get_hash(key))].get_head_node()
        if not chain_cur:
            self._arr[self._compress(self._get_hash(key))].insert_to_back(entry)
            self._size += 1
            return
        while chain_cur:
            if chain_cur.get_data().get_key() == key:
                old_value = chain_cur.get_data().get_value()
                chain_cur.set_data(entry)
                return old_value 
            chain_cur = chain_cur.get_next()
        self._arr[self._compress(self._get_hash(key))].insert_to_back(entry)
        self._size += 1

    def insert_kv(self, key: Any, value: Any) -> Any | None:
        """
        A version of insert which takes a key and value explicitly.
        Handy if you wish to provide keys and values directly to the insert
        function. It will return the value returned by insert, so keep this
        in mind. You can modify this if you want, as long as it behaves.
        Time complexity for full marks: O(1*)
        """
        entry = Entry(key, value)
        self.insert(entry)

    def _get_hash(self, key: Any) -> int:
        byte_array = object_to_byte_array(key)
        return int.from_bytes(byte_array, byteorder='big') # byteorder only default argument as of 3.11, autograder 3.10

    def _compress(self, key: Any) -> int:
        return key % self._primes[self._prime_index]

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        For convenience, you may wish to use this as an alternative
        for insert as well. However, this version does _not_ return
        anything. Can be used like: my_map[some_key] = some_value
        Time complexity for full marks: O(1*)
        """
        self.insert_kv(key, value)

    def get_load_factor(self) -> float:
        return self.get_size() / self._primes[self._prime_index]

    def remove(self, key: Any) -> None:
        """
        Remove the key/value pair corresponding to key k from the
        data structure. Don't return anything.
        Time complexity for full marks: O(1*)
        """
        if self._arr[self._compress(self._get_hash(key))].find_and_remove_element(key):
            self._size -= 1

    def find(self, key: Any) -> Any | None:
        """
        Find and return the value v corresponding to key k if it
        exists; return None otherwise.
        Time complexity for full marks: O(1*)
        """
        chain_cur = self._arr[self._compress(self._get_hash(key))].get_head_node()
        while chain_cur:
            if chain_cur.get_data().get_key() == key:
                return chain_cur.get_data().get_value() 
            chain_cur = chain_cur.get_next()
        return

    def __getitem__(self, key: Any) -> Any | None:
        """
        For convenience, you may wish to use this as an alternative
        for find()
        Time complexity for full marks: O(1*)
        """
        return self.find(key)

    def get_size(self) -> int:
        """
        Time complexity for full marks: O(1)
        """
        return self._size

    def is_empty(self) -> bool:
        """
        Time complexity for full marks: O(1)
        """
        return self._size == 0
