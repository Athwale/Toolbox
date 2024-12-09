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


def test_evaluate_on():
    comments, output = process_conditions(Path('./input-0.ks'), 'test', True)
    assert comments == ['test test']
    assert output.getvalue() == "echo 'test' >> testfile\n#CONDITION test IS TURNED ON\nsed -s\necho 'done'"
    output.close()


def test_evaluate_on_alt_name():
    comments, output = process_conditions(Path('./input-1.ks'), 'test', True)
    assert comments == ['test1', 'test2']
    assert '#$$ if: test1 - test 1\n' in output.getvalue()
    output.close()


def test_evaluate_off():
    comments, output = process_conditions(Path('./input-0.ks'), 'test', False)
    assert comments == ['test test']
    assert output.getvalue() == ("echo 'test' >> testfile\nif [ 1 -eq 1 ]; then\necho 'yes'\nfi\n# TEST\nCONDITION test"
                                 " IS TURNED OFF\necho 'done'")
    output.close()







