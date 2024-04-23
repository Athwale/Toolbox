import pytest

from pathlib import Path
from parametrize import validate
from parametrize import process_conditions


def test_validate_ok():
    assert validate(Path('./test-0.ks')) == (True, 0, '')


def test_validate_wrong_keyword():
    assert validate(Path('./test-1.ks')) == (False, 5, 'Unrecognized keyword')


def test_validate_multiple_else():
    assert validate(Path('./test-3.ks')) == (False, 4, 'Multiple else statements')


def test_validate_stray_if():
    assert validate(Path('./test-4.ks')) == (False, 2, 'Stray if')


def test_validate_stray_if_1():
    assert validate(Path('./test-6.ks')) == (False, 4, 'Stray if')


def test_validate_stray_if_2():
    assert validate(Path('./test-7.ks')) == (False, 6, 'Stray if')


def test_validate_stray_fi():
    assert validate(Path('./test-2.ks')) == (False, 7, 'Stray fi')


def test_validate_stray_else():
    assert validate(Path('./test-5.ks')) == (False, 7, 'Stray else')


def test_evaluate():
    assert validate(Path('./test-5.ks')) == (False, 7, 'Stray else')










