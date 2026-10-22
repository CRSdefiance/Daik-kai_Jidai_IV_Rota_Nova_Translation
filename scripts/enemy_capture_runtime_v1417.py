"""One original capture caller in the existing selector/gate allocations.

The old codec used numeric bias384. Moving numeric bias to512 saves four
padding bytes across the four numeric rows. Pointer bias stays896. The gate
adjusts the three historical numeric dispatch thresholds by exactly128.
All high-word memberships must remain disjoint from those special thresholds.
No selector is broadened and no allocation grows.
"""
import inspect
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import ship_sinking_runtime_v1328 as previous
from scripts import battle_aftermath_runtime_v1253 as codec

BASE = 0x02000000
SOURCE = 'e804968623fea7cd645fa78d34d53517374c6ff8df9a421ff40515fa7991bdd3'
CONTRACTS,GATE = previous.CONTRACTS,previous.GATE
TABLE_BYTES,GATE_BYTES = 188,172
NUMERIC_BIAS,POINTER_BIAS = 512,896

def contract_rows():
    rows = []
    for p,o,h,values in previous.contract_rows():
        if p==0x02053F40:
            assert h==0x0211 and 0x7B00 not in values
            values = tuple(sorted((*values,0x7B00)))
        rows.append((p,o,h,values))
    return rows

def rebased(fn,*args):
    source = inspect.getsource(fn)
    assert source.count('else 384')==1
    source = source.replace('else 384','else 512')
    env = dict(codec.__dict__)
    exec(compile(source,__file__,'exec'),env)
    return env[fn.__name__](*args)

def table():
    value = rebased(codec.encode,contract_rows())
    rows,end = rebased(codec.decode,value)
    assert rows==contract_rows() and end==len(value)==186
    return value+bytes(TABLE_BYTES-len(value))

def gate():
    _,assembly = codec.gate()
    for old,new in [
        ('movs r7,#2\nlsls r7,r7,#8\nsubs r3,r3,r7','movs r7,#3\nlsls r7,r7,#7\nsubs r3,r3,r7'),
        ('ready:\nsubs r3,#192\nsubs r3,#192','ready:\nsubs r3,#255\nsubs r3,#255\nsubs r3,#2'),
        ('movs r4,#229\nlsls r4,r4,#1','movs r4,#165\nlsls r4,r4,#1')]:
        assert assembly.count(old)==1,old
        assembly = assembly.replace(old,new)
    specials = {842-512,905-512,906-512,1028-512,1029-512}
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
    assert arm[GATE-BASE:GATE-BASE+GATE_BYTES]==codec.gate()[0]
    target = bytearray(arm)
    patches = []
    for at,value in [(CONTRACTS,table()),(GATE,gate()[0])]:
        source = arm[at-BASE:at-BASE+len(value)]
        target[at-BASE:at-BASE+len(value)] = value
        patches.append({'address':at,'source_hex':source.hex(),'target_hex':value.hex()})
    target = bytes(target)
    restored = bytearray(target)
    for patch in patches:
        at = patch['address']-BASE
        restored[at:at+len(bytes.fromhex(patch['source_hex']))] = bytes.fromhex(patch['source_hex'])
    assert bytes(restored)==arm
    old,new = [MainCodeFile(v,BASE) for v in [arm,target]]
    shape = lambda obj:[(s.ramAddress,len(s.data),s.bssSize) for s in obj.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(target)
    assert all(old.sections[i].data==new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48==123040
    return target,{'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),'patches':patches,
        'private_spans':[[CONTRACTS,CONTRACTS+TABLE_BYTES],[GATE,GATE+GATE_BYTES]],
        'encoded_table_bytes':186,'owned_table_bytes':188,'native_gate_bytes':172,'owned_gate_bytes':172,
        'new_memberships':[{'parent':0x02053F40,'stack_selector_offset':0x274,'table':0x02117B00}],
        'numeric_encoding_bias':512,'pointer_encoding_bias':896,'old_numeric_encoding_bias':384,
        'all_other_memberships_and_all8_parent_stack_high_word_contracts_exact':True,
        'all_nonowned_ARM9_bytes_restore_exact':True,
        'sections_BSS_cache_ITCM_arena_and123040_staged_bytes_exact':True,
        'gate_assembly':gate()[1],'research_only_no_ROM_registry_or_completion_change':True}
