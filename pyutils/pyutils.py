#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions and classes that fall within the Python standard library.
"""

import re
from collections.abc import Iterable

def camel_to_snake(inp_str):
    """
    Converts a string from camel case to snake case (Ex TestVar => test_var).
    See the following for the full stackoverflow page:
        https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case

    Parameters
    ----------
    inp_str : str
        The inputted string that is in camel case.

    Returns
    -------
    str : str
        Inputted string in snake case.
    """
    res_str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', inp_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', res_str).lower()


def as_list(obj, length=None, tp=None, iter_to_list=True):
    """
    Force an argument to be a list, optionally of a given length, optionally
    with all elements cast to a given type if not None.

    Paramters
    ---------
    obj : Object
    	The obj we want to convert to a list.

    length : int or None, optional
    	Length of new list. Applies if the inputted obj is not an iterable and
    	iter_to_list is false.

    tp : type, optional
    	Type to cast the values inside the list as.

    iter_to_list : bool, optional
    	Determines if we should cast an iterable (not str) obj as a list or to
    	enclose it in one.

    Returns
    -------
    obj : list
    	The object enclosed or cast as a list.
    """
    # If the obj is None, return empty list or fixed-length list of Nones
    if obj is None:
        if length is None:
            return []
        return [None] * length
    
    # If it is already a list do nothing
    elif isinstance(obj, list):
        pass

    # If it is an iterable (and not str), convert it to a list
    elif isiterable(obj) and iter_to_list:
        obj = list(obj)
        
    # Otherwise, just enclose in a list making it the inputted length
    else:
        try:
            obj = [obj] * length
        except TypeError:
            obj = [obj]
        
    # Cast to type; Let exceptions here bubble up to the top.
    if tp is not None:
        obj = [tp(o) for o in obj]
    return obj

def isiterable(obj):
    """
    Function that determines if an object is an iterable, not including 
    str.

    Parameters
    ----------
    obj : object
        Object to test if it is an iterable.

    Returns
    -------
    bool : bool
        True if the obj is an iterable, False if not.
    """
    if isinstance(obj, str):
        return False
    else:
        return isinstance(obj, Iterable)

def isnumber(obj):
    """
    Checks if the input is a number.

    Parameters
    ----------
    obj : object
        Object to test if it is an number.

    Returns
    -------
    bool : bool
        True if the obj is a number, False if not.    
    """
    if isinstance(obj, str):
        try:
            float(obj)
            return True
        except ValueError:
            return False
    elif isinstance(obj, (float, int)):
        return True
    else:
        return False

def _flatten(inp_iter):
    """
    Recursively iterate through values in nested iterables.

    Parameters
    ----------
    inp_iter : iterable
        The iterable to flatten.

    Returns
    -------
    value : object
        The contents of the iterable
    """
    for val in inp_iter:
        if isiterable(val):
            for ival in _flatten(val):
                yield ival
        else:
            yield val

def flatten(inp_iter):
    """
    Returns a flattened list of the inputted iterator.

    Parameters
    ----------
    inp_iter : iterable
        The iterable to flatten.

    Returns
    -------
    flattened_iter : list
        The contents of the iterable as a flat list
    """
    return list(_flatten(inp_iter))

def isempty(inp_iter):
    """
    Checks if an iterable (nested or not) is empty.

    Parameters
    ----------
    inp_iter : iterable
        The iterable to check for emptiness.

    Returns
    -------
    bool : bool:
        True if the iterator empty, False if not.
    """
    return not any(1 for _ in _flatten(inp_iter))
