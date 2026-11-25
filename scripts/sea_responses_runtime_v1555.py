"""Exact role7 creature/ghost table membership without enlarging any owned bank."""
from types import FunctionType
from scripts import declaration_responses_runtime_v1534 as previous
from scripts import declaration_responses_runtime_v1534 as template

BASE = 0x02000000
SOURCE = '70db0ecba39fe235e5022280a59c3928a05a7def7a306875389d12149b11c966'
CONTRACTS, GATE = previous.CONTRACTS, previous.GATE
TABLE_BYTES, GATE_BYTES, NEW_KEY = 188, 172, 0x86E0


def contract_rows():
    rows, found = [], False
    for parent, offset, high, keys in previous.contract_rows():
        if parent == 0x02053DB8:
            assert high == 0x0211 and offset == 0x27C and NEW_KEY not in keys
            keys = tuple(sorted((*keys, NEW_KEY)))
            found = True
        rows.append((parent, offset, high, keys))
    assert found
    return rows


def table():
    bound = FunctionType(previous.table.__code__, {**previous.table.__globals__, 'contract_rows': contract_rows}, argdefs=previous.table.__defaults__)
    return bound()


def gate():
    return previous.gate()


def apply(arm):
    fn = FunctionType(template.apply.__code__, {**template.apply.__globals__, 'SOURCE': SOURCE, 'previous': previous,
        'contract_rows': contract_rows, 'table': table, 'gate': gate}, argdefs=template.apply.__defaults__)
    target, proof = fn(arm)
    proof['new_memberships'] = [{'parent': 0x02053DB8, 'stack_selector_offset': 0x27C, 'table': 0x021186E0}]
    return target, proof
