"""Keep compiler-generated breaks within the original foraging portraits."""

from types import FunctionType

from dk4tool.patch.clifford_declaration_wrap_v1 import transform as extend_portrait_selector


PRIOR, ENTRY = 0x01FFBA34, 0x01FFBCF0
PARENT, STACK_KEY, TABLE = 0x02053DB8, 0x27C, 0x02116E80


def transform(source, source_sha256):
    inherited = extend_portrait_selector
    scope = inherited.__globals__ | {
        "PRIOR": PRIOR, "ENTRY": ENTRY, "PARENT": PARENT, "STACK_KEY": STACK_KEY, "TABLE": TABLE,
    }
    return FunctionType(inherited.__code__, scope)(source, source_sha256)
