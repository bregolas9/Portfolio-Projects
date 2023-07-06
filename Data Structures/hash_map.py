# Name: Brendan Bordine
# OSU Email: bordineb@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 12/3/21
# Description: This assignment is the implementation of a HashMap which uses a a dynamic array to store a hash table.
# I wrote the functions for the HashMap from the given skeleton code.


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the contents of the hash map.
        """
        for i in range(0, self.capacity):
            self.buckets.set_at_index(i, LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.
        """
        SLL = self.buckets.get_at_index(self.hash_function(key) % self.capacity)
        if SLL.contains(key) == None:
            return None
        else:
            return SLL.contains(key).value

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map.
        """
        SLL = self.buckets.get_at_index(self.hash_function(key) % self.capacity)
        if SLL.length() == 0:
            SLL.insert(key, value)
        elif SLL.contains(key) != None:
            SLL.remove(key)
            SLL.insert(key, value)
            self.size -= 1
        else:
            SLL.insert(key, value)
        self.size += 1

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.
        """
        SLL = self.buckets[self.hash_function(key) % self.capacity].contains(key)
        if SLL == None:
            return
        else:
            self.buckets[self.hash_function(key) % self.capacity].remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False.
        """
        if self.buckets.get_at_index(self.hash_function(key) % self.capacity).contains(key) != None:
            return True
        return False

    def empty_buckets(self) -> int:
        """
        Returns how many empty buckets are in the Hash Table.
        """
        number_of_empties = 0
        for i in range(0, self.capacity):
            if self.buckets[i].head == None:
                number_of_empties += 1
        return number_of_empties

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        s = self.size
        c = self.capacity
        return s / c

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table.
        """
        if new_capacity < 1:
            return
        table = DynamicArray()
        for i in range(new_capacity):
            table.append(LinkedList())
        temp_SLL = LinkedList()
        for i in range(0, self.capacity):
            current = self.buckets.get_at_index(i)
            if current.length() == 0:
                continue
            else:
                for node in current:
                    temp_SLL.insert(node.key, node.value)
        temporary_flip = LinkedList()
        for node in temp_SLL:
            temporary_flip.insert(node.key, node.value)
        self.size, self.capacity, self.buckets = 0, new_capacity, table
        for node in temporary_flip:
            self.put(node.key, node.value)

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all keys stored in your hash map.
        """
        keys = DynamicArray()
        for i in range(self.buckets.length()):
            for j in self.buckets.get_at_index(i):
                keys.append(j.key)
        return keys