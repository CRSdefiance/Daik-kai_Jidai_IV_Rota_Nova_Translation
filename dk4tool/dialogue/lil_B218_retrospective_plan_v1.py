"""Exact B218 retrospective plan adapter;one paragraph receives a soft boundary preference."""
from types import FunctionType
from scripts import plan_lil_B218_layout_v6881c as inherited
def plan(row):
    if row['id']!='DK4_MES_B218_R0027':return inherited.plan(row)
    bound=FunctionType(inherited.plan.__code__,{**inherited.plan.__globals__,'PAIRS':inherited.PAIRS|{("that's","a")}},argdefs=inherited.plan.__defaults__)
    return bound(row)
