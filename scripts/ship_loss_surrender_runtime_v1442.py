"""Three proven role1 report tables inside the existing188/172 byte banks."""
import inspect
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import enemy_capture_runtime_v1417b as previous
from scripts import battle_aftermath_runtime_v1253 as codec

BASE = 0x02000000
SOURCE = '6e5ab942aa51ae0463d14c7e19e9c34521ad0715857ac05f8c41dc38afdd5b47'
CONTRACTS,GATE = previous.CONTRACTS,previous.GATE
TABLE_BYTES,GATE_BYTES = 188,172
NEW_KEYS = (0x7AC0,0x7B80,0x7C60)

def contract_rows():
    rows = []
    for p,o,h,values in previous.contract_rows():
        if p==0x02053DB8:
            assert h==0x0211 and o==0x27C and not set(NEW_KEYS)&set(values)
            values = tuple(sorted((*values,*NEW_KEYS)))
        rows.append((p,o,h,values))
    return rows

def rebased(fn,*args):
    source = inspect.getsource(fn)
    assert source.count('else 384')==1
    env = dict(codec.__dict__)
    exec(compile(source.replace('else 384','else 768'),__file__,'exec'),env)
    return env[fn.__name__](*args)

def table():
    value = rebased(codec.encode,contract_rows())
    rows,end = rebased(codec.decode,value)
    assert rows==contract_rows() and end==len(value)==182
    return value+bytes(TABLE_BYTES-len(value))

def gate():
    _,assembly = codec.gate()
    for old,new in [
        ('movs r7,#2\nlsls r7,r7,#8\nsubs r3,r3,r7','movs r7,#128\nsubs r3,r3,r7'),
        ('ready:\nsubs r3,#192\nsubs r3,#192','ready:\nsubs r3,#192\nsubs r3,#192\nsubs r3,#192\nsubs r3,#192'),
        ('movs r4,#229\nlsls r4,r4,#1','movs r4,#37\nlsls r4,r4,#1')]:
        assert assembly.count(old)==1,old
        assembly = assembly.replace(old,new)
    specials = {842-768,905-768,906-768,1028-768,1029-768}
    for p,o,h,values in contract_rows():
        if h:
            shift = 4 if p==0x02053C14 else 5
            assert not {(v>>shift)-896 for v in values}&specials
    code = bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,GATE)[0])
    assert len(code)==GATE_BYTES
    return code,assembly

def apply(arm):
    assert sha(arm)==SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES]==previous.table()
    assert arm[GATE-BASE:GATE-BASE+GATE_BYTES]==previous.gate()[0]
    target = bytearray(arm);patches = []
    for at,value in [(CONTRACTS,table()),(GATE,gate()[0])]:
        source = arm[at-BASE:at-BASE+len(value)]
        target[at-BASE:at-BASE+len(value)] = value
        patches.append({'address':at,'source_hex':source.hex(),'target_hex':value.hex()})
    target = bytes(target);restored = bytearray(target)
    for patch in patches:
        at = patch['address']-BASE;value = bytes.fromhex(patch['source_hex'])
        restored[at:at+len(value)] = value
    assert bytes(restored)==arm
    old,new = [MainCodeFile(v,BASE) for v in [arm,target]]
    shape = lambda obj:[(s.ramAddress,len(s.data),s.bssSize) for s in obj.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(target)
    assert all(old.sections[i].data==new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48==123040
    return target,{'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),'patches':patches,
        'private_spans':[[CONTRACTS,CONTRACTS+TABLE_BYTES],[GATE,GATE+GATE_BYTES]],
        'encoded_table_bytes':182,'owned_table_bytes':188,'native_gate_bytes':172,'owned_gate_bytes':172,
        'new_memberships':[{'parent':0x02053DB8,'stack_selector_offset':0x27C,'table':0x02110000+n} for n in NEW_KEYS],
        'numeric_encoding_bias':768,'pointer_encoding_bias':896,'old_numeric_encoding_bias':512,
        'all_prior_memberships_and_all8_parent_stack_high_word_contracts_exact':True,
        'all_nonowned_ARM9_bytes_restore_exact':True,'shared_balance_literal_and_live_status_helpers_exact':True,
        'sections_BSS_cache_ITCM_arena_and123040_staged_bytes_exact':True,'gate_assembly':gate()[1],
        'research_only_no_ROM_registry_or_completion_change':True}
