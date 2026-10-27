"""Add the single source-proven fire table within the existing188-byte bank."""
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import battle_aftermath_runtime_v1253 as previous

BASE = 0x02000000
SOURCE = 'd870a1baf517e77c6ee612d87c9a1b871b5b723685254689103f9199caf134ac'
CONTRACTS, GATE = previous.CONTRACTS, previous.GATE
TABLE_BYTES, GATE_BYTES = 188, 172


def contract_rows():
    rows = []
    for parent,offset,high,values in previous.contract_rows():
        if parent == 0x02053F40:
            assert high == 0x0211 and 0x7980 not in values
            values = tuple(sorted((*values,0x7980)))
        rows.append((parent,offset,high,values))
    return rows


def table():
    value = previous.encode(contract_rows())
    rows,end = previous.decode(value)
    assert rows == contract_rows() and end == len(value) == 186 and len(value) <= TABLE_BYTES
    return value+bytes(TABLE_BYTES-len(value))


def apply(arm):
    assert sha(arm) == SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES] == previous.table()
    assert arm[GATE-BASE:GATE-BASE+GATE_BYTES] == previous.gate()[0]
    target = bytearray(arm)
    target[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES] = table()
    target = bytes(target)
    old,new = (MainCodeFile(value,BASE) for value in [arm,target])
    shape = lambda obj:[(section.ramAddress,len(section.data),section.bssSize) for section in obj.sections]
    assert shape(old) == shape(new) and cache_plan(arm) == cache_plan(target)
    assert all(old.sections[i].data == new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48 == 123040
    assert target[:CONTRACTS-BASE] == arm[:CONTRACTS-BASE]
    assert target[CONTRACTS-BASE+TABLE_BYTES:] == arm[CONTRACTS-BASE+TABLE_BYTES:]
    return target,{'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),
        'patches':[{'address':CONTRACTS,'source_hex':previous.table().hex(),'target_hex':table().hex()}],
        'private_spans':[[CONTRACTS,CONTRACTS+TABLE_BYTES],[GATE,GATE+GATE_BYTES]],
        'encoded_table_bytes':186,'owned_table_bytes':188,'native_gate_bytes':168,'owned_gate_bytes':172,
        'only_one_new_membership':{'parent':0x02053F40,'table':0x02117980},
        'existing_gate_code_all_other_ARM9_status_phrases_and_suffix_exact':True,
        'sections_BSS_cache_ITCM_arena_and123040_staged_bytes_exact':True,
        'research_only_no_ROM_registry_or_completion_change':True}
