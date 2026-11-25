"""The exact added low key needs186 bytes;185 assertion wrote no output."""
from types import FunctionType
from scripts import retreat_transfer_runtime_v1509 as previous
from scripts.retreat_transfer_runtime_v1509 import BASE,SOURCE,CONTRACTS,GATE,TABLE_BYTES,GATE_BYTES,NEW_KEY,contract_rows,gate

def table():
    codec=previous.previous.previous.previous.codec
    value=previous.previous.previous.rebased(codec.encode,contract_rows())
    rows,end=previous.previous.previous.rebased(codec.decode,value)
    assert rows==contract_rows() and end==len(value)==186
    return value+bytes(TABLE_BYTES-len(value))

def apply(arm):
    bound=FunctionType(previous.apply.__code__,{**previous.__dict__,'table':table},argdefs=previous.apply.__defaults__)
    target,proof=bound(arm)
    proof.update(encoded_table_bytes=186,packing185_assumption_rejected_before_any_payload_output=True)
    return target,proof
