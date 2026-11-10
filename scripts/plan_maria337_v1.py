"""Retain the full-width source/byte/parity planner for335 fixed-selector bodies."""
from scripts import plan_maria330_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous.source,{
    'work/Maria_B96_B124_clean_20261109':'work/Maria_B125_B136_clean_20261109',
    "doc['physical_speech_objects']==328":"doc['physical_speech_objects']==335",
    "doc['blocks']==[96,98,99,100,101,102,103,104,105,106,107,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124]":"doc['blocks']==list(range(125,137))",
    "len(bound)==len(original)==len(doc['records'])==330":"len(bound)==len(original)==len(doc['records'])==337",
    'assert len(bindings)==328':'assert len(bindings)==335',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-full-width-controls-phase-andpagination-contract','exec'),globals())
