"""Correct the research length assumption:rebasing saves two net bytes.

V1417 stopped before writing any payload because its186-byte estimate omitted
even-row padding. The decoded rows are exact and require188 owned bytes.
The gate remains172 bytes and no allocation grows.
"""
from types import FunctionType
from scripts import enemy_capture_runtime_v1417 as previous
from scripts.enemy_capture_runtime_v1417 import (BASE,SOURCE,CONTRACTS,GATE,
    TABLE_BYTES,GATE_BYTES,NUMERIC_BIAS,POINTER_BIAS,contract_rows,rebased,gate)

def table():
    value = rebased(previous.codec.encode,contract_rows())
    rows,end = rebased(previous.codec.decode,value)
    assert rows==contract_rows() and end==len(value)==TABLE_BYTES
    return value

def apply(arm):
    bound = FunctionType(previous.apply.__code__,{**previous.__dict__,'table':table},argdefs=previous.apply.__defaults__)
    target,plan = bound(arm)
    plan['encoded_table_bytes'] = 188
    plan['capacity_estimate_correction'] = '186 estimate rejected before output;exact even-row encoding is188 bytes'
    return target,plan
