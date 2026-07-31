import pytest

from dk4tool.insert.fixed_length import FixedInsertError, replace_fixed


def test_fixed_insert_shorter_pads_and_preserves_other_bytes():
    original = b"HEADJapaneseTAIL"
    rebuilt = replace_fixed(original, 4, 8, b"Yes")
    assert rebuilt == b"HEADYes\0\0\0\0\0TAIL"


def test_fixed_insert_overflow_rejected():
    with pytest.raises(FixedInsertError):
        replace_fixed(b"abcd", 0, 2, b"long")

