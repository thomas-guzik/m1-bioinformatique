# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
BitArray provides an easy manipulation for bit's array.
You can create the array specifying the number of bits it should contain.
"""


class BitArray:
    def __init__(self, n_bits):
        self.len = n_bits
        self.array = bytearray(n_bits)
    
    def get_position(self, i):
        """Return the position of the i-th bit in an array grouping by offset"""
        return i % 8
    
    def get_offset(self, i):
        """Return the position of the offset for a given i"""
        return i // 8
    
    def set_i(self, i, value):
        """Set the i-th bit in the array to 1 or 0"""
        offset = self.get_offset(i)
        position = self.get_position(i)
        byte = self.array[offset]
        mask = value << position
        self.array[offset] = byte | mask
    
    def get_i(self, i):
        """Get the i-th bit in the array"""
        offset = self.get_offset(i)
        position = self.get_position(i)
        byte = self.array[offset]
        mask = 1 << position
        return byte & mask
    
    def get_bytes(self):
        return bytes(self.array)
