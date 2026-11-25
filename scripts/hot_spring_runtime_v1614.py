"""Two original hot-spring tables in existing188/172-byte native banks."""
import inspect
from pathlib import Path
from ndspy.code import MainCodeFile
from keystone import Ks,KS_ARCH_ARM,KS_MODE_THUMB
from scripts import sea_responses_runtime_v1555 as previous
from scripts.ship_loss_surrender_runtime_v1442 import codec
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import save

BASE=0x02000000
SOURCE='794fe8829885f750f57c9720ea213c48da7feca7ee0b4d6869a63858a7a461a1'
CONTRACTS,GATE=previous.CONTRACTS,previous.GATE
TABLE_BYTES,GATE_BYTES=188,172
POINTER_BIAS,NUMERIC_BIAS=873,780
NEW_KEYS=(0x6D60,0x6D80)

def contract_rows():
    rows=[];found=False
    for parent,offset,high,keys in previous.contract_rows():
        if parent==0x02053DB8:
            assert (offset,high)==(0x27C,0x0211) and not set(keys)&set(NEW_KEYS)
            keys=tuple(sorted((*keys,*NEW_KEYS)));found=True
        rows.append((parent,offset,high,keys))
    assert found
    return rows

def rebased(fn,*args):
    source=inspect.getsource(fn);old='896 if high else 384';assert source.count(old)==1
    env=dict(codec.__dict__);exec(compile(source.replace(old,'873 if high else 780'),__file__,'exec'),env)
    return env[fn.__name__](*args)

def table():
    value=rebased(codec.encode,contract_rows());rows,end=rebased(codec.decode,value)
    assert rows==contract_rows() and end==len(value)==TABLE_BYTES
    return value

def gate():
    old,assembly=previous.gate();needle='pointer_bias:\nmovs r7,#116\nsubs r3,r3,r7'
    assert assembly.count(needle)==1
    assembly=assembly.replace(needle,'pointer_bias:\nmovs r7,#93\nsubs r3,r3,r7')
    code=bytes(Ks(KS_ARCH_ARM,KS_MODE_THUMB).asm(assembly,GATE)[0]);assert len(code)==168
    value=code+b'\xc0\x46'*2
    assert len(value)==GATE_BYTES and sum(a!=b for a,b in zip(old,value,strict=True))==1
    return value,assembly

def apply(arm):
    assert sha(arm)==SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES]==previous.table()
    assert arm[GATE-BASE:GATE-BASE+GATE_BYTES]==previous.gate()[0]
    specials={842-780,905-780,906-780,1028-780,1029-780}
    for parent,offset,high,keys in contract_rows():
        if high:
            shift=4 if parent==0x02053C14 else 5
            assert not {(key>>shift)-POINTER_BIAS for key in keys}&specials
    target=bytearray(arm);patches=[]
    for at,value in [(CONTRACTS,table()),(GATE,gate()[0])]:
        old=arm[at-BASE:at-BASE+len(value)];target[at-BASE:at-BASE+len(value)]=value
        patches.append({'address':at,'source_hex':old.hex(),'target_hex':value.hex()})
    target=bytes(target);restored=bytearray(target)
    for p in patches:
        at=p['address']-BASE;restored[at:at+len(bytes.fromhex(p['source_hex']))]=bytes.fromhex(p['source_hex'])
    assert bytes(restored)==arm
    old,new=[MainCodeFile(v,BASE) for v in [arm,target]]
    shape=lambda obj:[(s.ramAddress,len(s.data),s.bssSize) for s in obj.sections]
    assert shape(old)==shape(new) and cache_plan(arm)==cache_plan(target)
    assert all(old.sections[i].data==new.sections[i].data for i in [1,2,3,4])
    assert len(new.sections[3].data)-48==123040
    return target,{'source_ARM9_sha256':sha(arm),'target_ARM9_sha256':sha(target),'patches':patches,
        'private_spans':[[CONTRACTS,CONTRACTS+TABLE_BYTES],[GATE,GATE+GATE_BYTES]],
        'encoded_table_bytes':188,'owned_table_bytes':188,'native_gate_bytes':168,'owned_gate_bytes':172,
        'new_memberships':[{'parent':0x02053DB8,'stack_selector_offset':0x27C,'table':0x02110000+k} for k in NEW_KEYS],
        'numeric_encoding_bias':780,'pointer_encoding_bias':873,'old_pointer_encoding_bias':896,
        'only_one_gate_immediate_byte_changed_to_preserve_normalized_semantics':True,
        'gate_assembly':gate()[1],'all_prior_memberships_and_all8_parent_stack_high_word_contracts_exact':True,
        'all_prior_and_new_pointer_keys_disjoint_from_numeric_special_dispatch_values':True,
        'all_nonowned_ARM9_bytes_restore_exact':True,'sections_BSS_cache_ITCM_arena_and123040_staged_bytes_exact':True,
        'research_only_no_ROM_registry_or_completion_change':True}

if __name__=='__main__':
    root=Path('work/analysis/hot_spring_runtime_plan_v1614');assert not root.exists()
    arm=NdsImage.open('out/screenshot_text_repairs_20261022_candidate.nds').read_file('/__arm9__.bin');target,proof=apply(arm)
    root.mkdir(parents=True);path=root/'ARM9_RUNTIME_RESEARCH_ONLY.bin';path.write_bytes(target)
    save(root/'runtime_plan.json',{**proof,'research_ARM9':str(path),'runtime_module_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Two exact original role1 memberships added:188 selector/172 gate/123040 staged bytes fixed;one normalization immediate changes;exhaustive native verification pending.')
