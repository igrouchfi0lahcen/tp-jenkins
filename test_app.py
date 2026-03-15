from app import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(2, 3) == 5

