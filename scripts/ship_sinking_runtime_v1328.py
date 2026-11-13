"""Two original sinking consumers in the existing188-byte selector bank."""
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import powder_fire_runtime_v1307 as previous
from scripts.battle_aftermath_runtime_v1253 import encode,decode

BASE = 0x02000000
SOURCE = 'e1f66bfeb3a7debd83ea46dc714d900171dd1684d583cb3292b0682720131560'
CONTRACTS,GATE = previous.CONTRACTS,previous.GATE
TABLE_BYTES,GATE_BYTES = 188,172


def contract_rows():
    rows = []
    for parent,offset,high,values in previous.contract_rows():
        added = {0x02053DB8:0x79C0,0x02053F40:0x7A80}.get(parent)
        if added is not None:
            assert high==0x0211 and added not in values
            values = tuple(sorted((*values,added)))
        rows.append((parent,offset,high,values))
    return rows


def table():
    value = encode(contract_rows())
    rows,end = decode(value)
    assert rows==contract_rows() and end==len(value)==TABLE_BYTES
    return value


def apply(arm):
    assert sha(arm)==SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES]==previous.table()
    target = bytearray(arm)
    target[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES] = table()
    target = bytes(target)
    old,new = [MainCodeFile(value,BASE) for value in [arm,target]]
    shape = lambda obj:[(s.ramAddress,len(s.data),s.bssSize) for s in obj.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(target)
    assert all(old.sections[i].data==new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48==123040
    assert target[:CONTRACTS-BASE]==arm[:CONTRACTS-BASE]
    assert target[CONTRACTS-BASE+TABLE_BYTES:]==arm[CONTRACTS-BASE+TABLE_BYTES:]
    return target,{'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),
        'patches':[{'address':CONTRACTS,'source_hex':previous.table().hex(),'target_hex':table().hex()}],
        'private_spans':[[CONTRACTS,CONTRACTS+TABLE_BYTES],[GATE,GATE+GATE_BYTES]],
        'encoded_table_bytes':188,'owned_table_bytes':188,'native_gate_bytes':168,'owned_gate_bytes':172,
        'two_new_memberships':[{'parent':0x02053DB8,'table':0x021179C0},{'parent':0x02053F40,'table':0x02117A80}],
        'all_gate_code_other_ARM9_status_phrases_and_suffix_exact':True,
        'sections_BSS_cache_ITCM_arena_and123040_staged_bytes_exact':True,
        'research_only_no_ROM_registry_or_completion_change':True}
