"""Four actor tables in184 of188 selector bytes;the existing gate stays exact."""
from ndspy.code import MainCodeFile
from scripts import ship_loss_surrender_runtime_v1442b as previous
from scripts.research_reaction_scope_capacity_v1482 import contract_rows
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan

BASE=0x02000000
SOURCE='bd67129af50a558de5bfa2d82dbf6b6128ef11b5939e9e4bb350c238b05aa39d'
CONTRACTS,GATE=previous.CONTRACTS,previous.GATE
TABLE_BYTES,GATE_BYTES=188,172
NEW_KEYS=(0x7F40,0x7F80,0x8000,0x8060)

def table():
    codec=previous.previous.codec
    value=previous.rebased(codec.encode,contract_rows())
    rows,end=previous.rebased(codec.decode,value)
    assert rows==contract_rows() and end==len(value)==184
    return value+bytes(TABLE_BYTES-len(value))

def gate():return previous.gate()

def apply(arm):
    assert sha(arm)==SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES]==previous.table()
    assert arm[GATE-BASE:GATE-BASE+GATE_BYTES]==previous.gate()[0]
    target=bytearray(arm);patches=[]
    for at,value in [(CONTRACTS,table()),(GATE,gate()[0])]:
        source=arm[at-BASE:at-BASE+len(value)]
        target[at-BASE:at-BASE+len(value)]=value
        patches.append({'address':at,'source_hex':source.hex(),'target_hex':value.hex()})
    target=bytes(target);restored=bytearray(target)
    for patch in patches:
        at=patch['address']-BASE;value=bytes.fromhex(patch['source_hex'])
        restored[at:at+len(value)]=value
    assert bytes(restored)==arm
    old,new=[MainCodeFile(v,BASE) for v in [arm,target]]
    shape=lambda x:[(s.ramAddress,len(s.data),s.bssSize) for s in x.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(target)
    assert all(old.sections[i].data==new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48==123040
    return target,{'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),'patches':patches,
        'private_spans':[[CONTRACTS,CONTRACTS+TABLE_BYTES],[GATE,GATE+GATE_BYTES]],
        'encoded_table_bytes':184,'owned_table_bytes':188,'native_gate_bytes':168,'owned_gate_bytes':172,
        'new_memberships':[{'parent':0x02053F40,'stack_selector_offset':0x274,'table':0x02110000+k} for k in NEW_KEYS],
        'numeric_encoding_bias':780,'pointer_encoding_bias':896,'old_numeric_encoding_bias':780,
        'original172_byte_gate_exact':True,'gate_assembly':gate()[1],
        'all_prior_memberships_and_all8_parent_stack_high_word_contracts_exact':True,
        'all_nonowned_ARM9_bytes_restore_exact':True,'shared_balance_literal_and_live_status_helpers_exact':True,
        'sections_BSS_cache_ITCM_arena_and123040_staged_bytes_exact':True,
        'research_only_no_ROM_registry_or_completion_change':True}
