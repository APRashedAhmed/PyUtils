"""
Conftest for the tests in PyUtils
"""
############
# Standard #
############
import re
import logging
from collections.abc import Iterable

###############
# Third Party #
###############
import pytest
import numpy as np

##########
# Module #
##########
from pyutils import pyutils

test_values = [2, np.pi, True, "test_s", "10", ["test"], ("test",), {"test":1}]
test_lists = [[1,2,3,4,5], [[1],[2],[3],[4],[5]], [[1,2,3],[4,5]],
              [[1,[2,[3,[4,[5]]]]]]])

def test_camel_txo_snake_works_correctly():
    test_strings = ["TestStr", "LongTestStr", "ReallyLongTestStr"]
    true_strings = ["test_str", "long_test_str", "really_long_test_str"]
    for test_str, true_str in zip(test_strings, true_strings):
        assert pyutils.camel_to_snake(test_str) == true_str
 
@pytest.mark.parametrize("test", test_values)
def test_as_list_turns_inputs_to_lists(test):
    assert isinstance(pyutils.as_list(test), list)

@pytest.mark.parametrize("test", test_values)
def test_isiterable_correctly_returns(test):
    iterable = pyutils.isiterable(test)
    if isinstance(test, str):
        assert iterable is False
    elif isinstance(test, Iterable):
        assert iterable is True
    else:
        assert iterable is False

@pytest.mark.parametrize("test", test_values)
def test_isnumber_correctly_returns(test):
    isnumber = pyutils.isnumber(test)
    if isinstance(test, (float, int)):
        assert isnumber is True
    elif isinstance(test, str):
        try:
            float(test)
            return True
        except ValueError:
            return False  
    else:
        assert isnumber is False

@pytest.mark.parametrize("test", test_list)
def test_flatten_works_correctly(test):
    assert pyutils.flatten(test) == [1,2,3,4,5]



