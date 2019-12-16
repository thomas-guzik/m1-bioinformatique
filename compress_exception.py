# !/usr/bin/python
# -*- coding: utf-8 -*-


import argparse

class CompressException(Exception):
    def __init__(self, message=""):
        self.msg = message
    
    def __str__(self):
        return self.msg

class KmerSizeError(CompressException):
    pass

class BloomFilterSizeError(CompressException):
    pass


class BloomHashSizeError(CompressException):
    pass


class ProbabilitySizeError(CompressException):
    pass


class ImpreciseBloomFilterError(CompressException):
    pass


class ZeroOutputChoiceError(CompressException):
    pass

