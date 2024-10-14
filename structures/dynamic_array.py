"""
Skeleton for COMP3506/7505 A1, S2, 2024
The University of Queensland
Joel Mackenzie and Vladimir Morozov
"""

from typing import Any
from collections.abc import Iterator
from random import randint

class DynamicArray:
    def __init__(self) -> None:
        self._data = [None] * 128
        self._size = 0
        self._capacity = 128
        self._start = 64
        self._reversed = False

    def __get_index(self, index: int) -> int:
        """
        Return the actual index based on reversal
        """
        if not self._reversed:
            return (self._start + index)
        return (self._start + self._size - 1) - index

    def __internal_to_user_index(self, index: int) -> int:
        """
        Given an internal index, convert it to the corresponding user-observed
        index
        """
        if not self._reversed:
            return index - self._start
        return index - (self._start + self._size - 1)

    def iterate(self) -> Iterator[Any]:
        """
        We can use a special "iterate" generator to walk the correct direction
        depending on whether our list is reversed or not
        """
        for idx in range(self._size):
            logical_index = self.__get_index(idx)
            yield self._data[logical_index]

    def _iterate_indexes(self) -> Iterator[Any]:
        """
        We can use a special "iterate" generator to walk the correct direction
        depending on whether our list is reversed or not; this one returns
        the index of the elements, not the elements themselves
        """
        for idx in range(self._size):
            logical_index = self.__get_index(idx)
            yield logical_index


    def __str__(self) -> str:
        """
        A helper that allows you to print a DynamicArray type
        via the str() method.
        """
        string_rep = "["
        for elem in self.iterate():
            string_rep += str(elem) + ", "
        string_rep += "]"
        return string_rep

    def __resize(self) -> None:
        self._capacity = self._capacity * 2
        new_list = [None] * self._capacity
        new_start = self._capacity // 3
        for i in range(self._size):
            new_list[new_start + i] = self._data[self._start + i]
        self._start = new_start
        self._data = new_list

    def build_from_list(self, inlist: list) -> None:
        self._data = inlist
        self._start = 0
        self._capacity = len(inlist)
        self._size = len(inlist)

    def allocate(self, elements_desired: int, default_val: Any) -> None:
        """
        Allow the user to allocate a slab of elements at once, all
        initialized to the default value
        """
        self._data = [default_val] * elements_desired
        self._size = elements_desired
        self._capacity = elements_desired
        self._start = 0

    def get_at(self, index: int) -> Any | None:
        """
        Get element at the given index.
        Return None if index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index >= 0 and index < self._size:
            index = self.__get_index(index)
            return self._data[index]
        return None

    def __getitem__(self, index: int) -> Any | None:
        """
        Same as get_at.
        Allows to use square brackets to index elements.
        """
        return self.get_at(index)

    def set_at(self, index: int, element: Any) -> None:
        """
        Get element at the given index.
        Do not modify the list if the index is out of bounds.
        Time complexity for full marks: O(1)
        """
        if index >= 0 and index < self._size:
            index = self.__get_index(index)
            self._data[index] = element

    def __setitem__(self, index: int, element: Any) -> None:
        """
        Same as set_at.
        Allows to use square brackets to index elements.
        """
        self.set_at(index, element)

    def __append_to_back(self, element: Any) -> None:
        """
        Helper that adds an element to the end of the current space; does not
        care about reversal, just puts the element at the back
        """
        fwd_size = self._capacity - (self._start + self._size)
        if fwd_size == 0:
            self.__resize()
        self._data[self._start + self._size] = element
        self._size += 1

    def append(self, element: Any) -> None:
        """
        Add an element to the back of the array.
        Time complexity for full marks: O(1*) (* means amortized)
        """
        if self._reversed:
            self.__prepend_to_front(element)
        else:
            self.__append_to_back(element)

    def __prepend_to_front(self, element: Any) -> None:
        """
        Helper that adds an element to the front of the current space; does not
        care about reversal, just puts the element at the front
        """
        bck_size = self._start
        if bck_size == 0:
            self.__resize()
        self._start = self._start - 1
        self._data[self._start] = element
        self._size += 1


    def prepend(self, element: Any) -> None:
        """
        Add an element to the front of the array.
        Time complexity for full marks: O(1*)
        """
        if self._reversed:
            self.__append_to_back(element)
        else:
            self.__prepend_to_front(element)

    def reverse(self) -> None:
        """
        Reverse the array.
        Time complexity for full marks: O(1)
        """
        self._reversed = not self._reversed

    def remove(self, element: Any) -> None:
        """
        Remove the first occurrence of the element from the array.
        If there is no such element, leave the array unchanged.
        Time complexity for full marks: O(N)
        """
        found_idx = -1
        for idx in self._iterate_indexes():
            if self._data[idx] == element:
                self.remove_at(self.__internal_to_user_index(idx))
                return 

    def remove_at(self, index: int) -> Any | None:
        """
        Remove the element at the given index from the array and return the removed element.
        If there is no such element, leave the array unchanged and return None.
        Time complexity for full marks: O(N)
        """
        elem = None
        if index >= 0 and index < self._size:
            index = self.__get_index(index)
            elem = self._data[index]
            for i in range(index, self._start + self._size - 1):
                self._data[i] = self._data[i + 1]
            self._size -= 1
            self._data[self._start + self._size] = None
        return elem

    def is_empty(self) -> bool:
        """
        Boolean helper to tell us if the structure is empty or not
        Time complexity for full marks: O(1)
        """
        return self._size == 0

    def is_full(self) -> bool:
        """
        Boolean helper to tell us if the structure is full or not
        Time complexity for full marks: O(1)
        """
        return self._size == self._capacity

    def get_size(self) -> int:
        """
        Return the number of elements in the list
        Time complexity for full marks: O(1)
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the total capacity (the number of slots) of the list
        Time complexity for full marks: O(1)
        """
        return self._capacity

    def sort(self) -> None:
        """
        Sort elements inside _data based on < comparisons.
        Time complexity for full marks: O(NlogN)
        """
        self._reversed = False # Reset the reversed flag. sort() will reorder the array anyway, 
                               # no need to make our lives harder by tracking this flag inside qsort
        self.__qsort(self._start, self._start + self._size - 1)

    def __qsort(self, lo: int, hi: int) -> None:
        """
        Randomized quicksort
        """
        if lo >= hi:
            return
        pivot = self.__random_pivot(lo, hi)
        self.__qsort(lo, pivot)
        self.__qsort(pivot + 1, hi)

    def __random_pivot(self, lo: int, hi: int) -> int:
        """
        Return the index of the pivot after shuffling elements into < and >
        """
        pidx = randint(lo, hi)
        pivot = self._data[pidx]
        left = lo - 1
        right = hi + 1

        # Loop until we've moved everything around the pivot into < and >
        # groups.
        while True:
            left += 1
            # Find an element smaller than the pivot
            while self._data[left] < pivot:
                left += 1

            right -= 1
            # Find an element greater than the pivot
            while self._data[right] > pivot:
                right -= 1

            # If true, we are done; it means the list is already segmented,
            # so back out at this point
            if left >= right:
                return right
            
            # Otherwise, we swap the elements and continue
            self._data[left], self._data[right] = self._data[right], self._data[left]

