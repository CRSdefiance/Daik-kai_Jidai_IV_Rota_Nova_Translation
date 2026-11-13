"""Protect the exact original replacement-ship role table inside existing banks."""
from ndspy.code import MainCodeFile
from scripts import battle_reaction_runtime_v1483 as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan

BASE=0x02000000
SOURCE='2bb0236eacbf93d55092d76b69c13e38c599ff095bc640516b2b4c64b0c6c95c'
CONTRACTS,GATE=previous.CONTRACTS,previous.GATE
TABLE_BYTES,GATE_BYTES=188,172
NEW_KEY=0x7080

def contract_rows():
    rows=[];found=False
    for parent,offset,high,keys in previous.contract_rows():
        if parent==0x02053DB8:
            assert high==0x0211 and offset==0x27C and NEW_KEY not in keys
            keys=tuple(sorted((*keys,NEW_KEY)));found=True
        rows.append((parent,offset,high,keys))
    assert found
    return rows

def table():
    codec=previous.previous.previous.codec
    value=previous.previous.rebased(codec.encode,contract_rows())
    rows,end=previous.previous.rebased(codec.decode,value)
    assert rows==contract_rows() and end==len(value)==185
    return value+bytes(TABLE_BYTES-len(value))

def gate():return previous.gate()

def apply(arm):
    assert sha(arm)==SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES]==previous.table()
    assert arm[GATE-BASE:GATE-BASE+GATE_BYTES]==gate()[0]
    specials={842-780,905-780,906-780,1028-780,1029-780}
    for parent,offset,high,keys in contract_rows():
        if high:
            shift=4 if parent==0x02053C14 else 5
            assert not {(key>>shift)-896 for key in keys}&specials
    target=bytearray(arm);patches=[]
    for at,value in [(CONTRACTS,table()),(GATE,gate()[0])]:
        old=arm[at-BASE:at-BASE+len(value)];target[at-BASE:at-BASE+len(value)]=value
        patches.append({'address':at,'source_hex':old.hex(),'target_hex':value.hex()})
    target=bytes(target);restored=bytearray(target)
    for patch in patches:
        at=patch['address']-BASE;value=bytes.fromhex(patch['source_hex']);restored[at:at+len(value)]=value
    assert bytes(restored)==arm
    old,new=[MainCodeFile(v,BASE) for v in [arm,target]]
    shape=lambda obj:[(s.ramAddress,len(s.data),s.bssSize) for s in obj.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(target)
    assert all(old.sections[i].data==new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48==123040
    return target,{'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),'patches':patches,
        'private_spans':[[CONTRACTS,CONTRACTS+TABLE_BYTES],[GATE,GATE+GATE_BYTES]],
        'encoded_table_bytes':185,'owned_table_bytes':188,'native_gate_bytes':168,'owned_gate_bytes':172,
        'new_memberships':[{'parent':0x02053DB8,'stack_selector_offset':0x27C,'table':0x02117080}],
        'numeric_encoding_bias':780,'pointer_encoding_bias':896,'old_numeric_encoding_bias':780,
        'original172_byte_gate_exact':True,'gate_assembly':gate()[1],
        'all_prior_memberships_and_all8_parent_stack_high_word_contracts_exact':True,
        'all_nonowned_ARM9_bytes_restore_exact':True,'shared_balance_literal_and_live_status_helpers_exact':True,
        'sections_BSS_cache_ITCM_arena_and123040_staged_bytes_exact':True,
        'research_only_no_ROM_registry_or_completion_change':True}
