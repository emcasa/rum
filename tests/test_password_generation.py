from rum.utils.password_generator import Password
import string
import pytest

alphabet = string.ascii_letters + string.digits + "-_=."


def test_password_length():
    password_lengths = [15, 20, 16, 40]

    for length in password_lengths:
        expected = length
        result = len(Password(length).generate())
        print(result)
        assert expected == result


def test_password_lower_than_minimal():
    with pytest.raises(ValueError):
        Password(8, 15)


def test_password_correct_type():
    expected = True
    password = Password(20).str

    for char in password:
        if char not in alphabet:
            expected = False

    assert expected


def test_password_incorrect_type():
    expected = True
    password = Password(20).str + '#'

    for char in password:
        if char not in alphabet:
            expected = False

    assert not expected

