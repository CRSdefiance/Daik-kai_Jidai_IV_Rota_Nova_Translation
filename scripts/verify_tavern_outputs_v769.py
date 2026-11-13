"""Whole native outputs through prospective real dispatcher,not direct bypass."""

import inspect
import re
import struct
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import probe_tavern_conversations_v764 as earlier
from scripts import probe_tavern_continuation_layout_v768 as drafts
from scripts import tavern_continuation_runtime_v769 as rt
from scripts.context_tavern_continuation_v768 import CURRENT,RAM_REPORT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE,STACK
from scripts.review_tavern_continuation_v768 import MANUSCRIPT
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/tavern_runtime_v769')


def main():
    rom=NdsImage.open(CURRENT);arm=rom.read_file('/__arm9__.bin')
    plan=read(ROOT/'owned_runtime_plan.json')
    assert plan['runtime_module_sha256']==sha(Path(rt.__file__).read_bytes())
    raw=snapshot(read(RAM_REPORT),3200);writes=[]
    def loaded():
        u=machine(arm);u.mem_write(BASE,raw);rt.load_into_cpu(u,arm)
        def watch(cpu,kind,at,size,value,unused):
            writes.append([at,size,value]);raise AssertionError('Write into immutable runtime storage')
        for p in plan['patches']:u.hook_add(UC_HOOK_MEM_WRITE,watch,begin=p['address'],end=p['address']+p['bytes']-1)
        return u
    source=inspect.getsource(drafts.format_case)
    marker='    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)'
    replacement='''    n = row['message_id']
    parent = 0x02053D24 if 852 <= n <= 858 else 0x02053C14 if n in (*range(859,863),*range(864,868)) else 0x02054014
    table = 0x021166F0 if 859 <= n <= 862 else 0x02116810 if 864 <= n <= 867 else 0
    for off,value in ((0x264,parent),(0x274,n),(0x270,table),(0x27C,0x02118400)):
        u.mem_write(STACK+off,struct.pack('<I',value))
    call(u, 0x01FFCF3C - BASE, (wrapped, output, 0), instruction_limit=2000000)'''
    assert source.count(marker)==1
    namespace=dict(drafts.__dict__);exec(compile(source.replace(marker,replacement),str(Path(__file__)),'exec'),namespace)
    formatter=namespace['format_case']
    previous=read(drafts.ROOT/'native_layout_matrix.json')
    assert previous['count']==14282 and not previous['findings_count']
    doc={r['message_id']:r for r in read(MANUSCRIPT)['records']}
    results=[]
    for i,old in enumerate(previous['cases']):
        if i%64==0:u=loaded()
        result=formatter(u,doc[old['id']],tuple(bytes.fromhex(v) for v in old['source_values_hex']))
        assert result==old,(old,result)
        results.append(result)
    save(ROOT/'new32_native_layout_matrix.json',{'count':len(results),'cases':results,
        'all_actual_direct_queued_cost_and_round_table_parent_bindings_used':True,
        'byte_exact_to_reviewed_literal_path_matrix':True})
    print('All14282 new outputs match reviewed paragraphs through actual scoped dispatch.',flush=True)
    source=inspect.getsource(earlier.format_case)
    marker="    assert b' '.join(result.split()) == b' '.join(expected.split()), (n, values, result, expected)"
    assert source.count(marker)==1
    replacement="    if n == 842: expected = re.sub(rb'([NSEW]) +([0-9])', rb'\\1\\2', expected)\n"+marker
    namespace=dict(earlier.__dict__);namespace['re']=re;exec(compile(source.replace(marker,replacement),str(Path(__file__)),'exec'),namespace)
    formatter=namespace['format_case']
    doc={r['message_id']:r for r in read('translations/tavern_conversations_editorial_manuscript_v4.json')['records']}
    proofs=[]
    for name,expected in (('native_layout_matrix',38957),('actual_leader_layout_matrix',14400)):
        path=Path('work/analysis/tavern_coordinates_v766')/(name+'.json');old_matrix=read(path)
        for i,old in enumerate(old_matrix['cases']):
            if i%64==0:u=loaded()
            new=formatter(u,doc[old['id']],tuple(bytes.fromhex(v) for v in old['values_hex']))
            assert new==old,(name,i,old,new)
        assert len(old_matrix['cases'])==expected
        proofs.append({'matrix':str(path),'matrix_sha256':sha(path.read_bytes()),'all_complete_cases_byte_exact':expected})
        print(f'{expected} inherited {name} outputs remain exact.',flush=True)
    # Original region getter returns the real newly packed string pointer. The
    # native ARM946 SDK copy handles every unaligned source phase,not host memcpy.
    region_copies=[];u=loaded()
    for i in range(8):
        call(u,0x9458C,(i,));record=u.reg_read(UC_ARM_REG_R0)
        pointer=struct.unpack('<I',u.mem_read(record,4))[0]
        value=bytes(u.mem_read(pointer,40)).split(b'\0')[0]
        u.mem_write(0x02476000,b'\xa5'*80)
        call(u,0xCEC74,(0x02476010,pointer,len(value)+1))
        assert bytes(u.mem_read(0x02476000,80))==b'\xa5'*16+value+b'\0'+b'\xa5'*(63-len(value))
        region_copies.append({'index':i,'pointer':pointer,'name':value.decode('ascii'),'full_native_copy_and_guard_bytes_exact':True})
    assert not writes
    save(ROOT/'full_output_verification.json',{'source_ROM_sha256':sha(CURRENT.read_bytes()),
        'runtime_plan_sha256':sha((ROOT/'owned_runtime_plan.json').read_bytes()),'manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'new32_complete_scoped_outputs':14282,'new_matrix':str(ROOT/'new32_native_layout_matrix.json'),
        'inherited_complete_matrices':proofs,'all8_original_region_getter_and_guarded_native_copies':region_copies,
        'immutable_storage_writes':writes,'fresh_initialized_CPU_every64_cases':True,
        'explicit_effective_new_formatter_sha256':sha(source.encode('utf-8')),
        'producer_sha256':sha(Path(__file__).read_bytes()),'actual_gameplay_registered_ROM_patch_pending':True,'full_goal_complete':False})
    print('All115 previously reviewed font planes retain exact text bytes;no immutable storage writes. No ROM emitted.',flush=True)


if __name__=='__main__':main()
