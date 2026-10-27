from __future__ import annotations

import pytest

from scripts.materialize_common_native_prefix_repairs import repair_prefix


@pytest.mark.parametrize("start", [1, 2])
def test_prefix_repair_preserves_paragraph_macros_and_break_guards(start):
    paragraph = b"%s has arrived.\n  Shall we help?"
    current = paragraph + b"    "
    source = b" " * start + b"x" * (len(current) - start)
    repaired = repair_prefix(source, current, start)
    assert len(repaired) == len(current)
    assert repaired[:start] == source[:start]
    assert repaired[start:].rstrip(b" ") == paragraph
    assert repaired.count(b"\n  ") == current.count(b"\n  ")


def test_prefix_repair_refuses_to_cut_prose_to_fit():
    with pytest.raises(ValueError, match="relocation required"):
        repair_prefix(b" " + b"x" * 5, b"Hello!", 1)


@pytest.mark.parametrize("source,current,start", [
    (b"\n xxx", b"Text ", 2),
    (b" xxx", b"Text  ", 1),
    (b" xxxx", b"A\0B  ", 1),
    (b" xxxx", b"\x82\xa0   ", 1),
])
def test_prefix_repair_rejects_unproven_or_packed_source(source, current, start):
    with pytest.raises(ValueError):
        repair_prefix(source, current, start)
