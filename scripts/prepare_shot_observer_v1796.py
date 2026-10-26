"""Source-bound,register-preserving read-only shot observation contract."""
import struct
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import CORE,CORE_SHA
from scripts.inspect_resource_dispatch_v668 import tables
from scripts.observe_file_requests_v681 import assemble
from scripts import check_file_requests_v681 as checker
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/shot_observer_contract_v1796')
ROM=Path('out/all_routes_combined_v1775_candidate.nds')
TARGETS=[(0x02073A44,'contact_predicate_return'),(0x02073B38,'flagship_pair_predicate'),
    (0x02073B5C,'lookout_Aim_return'),(0x02073B84,'native_roll_compare'),
    (0x02073BA0,'shot_announcement'),(0x02073BAC,'shot_message_return')]

if __name__=='__main__':
    assert not ROOT.exists();image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x732FC:0x74010]==clean[0x732FC:0x74010]
    raw=CORE.read_bytes();assert sha(raw)==CORE_SHA
    base,table=tables(raw);targets=[]
    for pc,name in TARGETS:
        word=struct.unpack_from('<I',arm,pc-0x02000000)[0];index=((word>>16)&0xFF0)|((word>>4)&15)
        targets.append({'PC':pc,'name':name,'word':word,'instruction_index':index,
            'handler_RVA':struct.unpack_from('<Q',raw,table['file_offset']+index*8)[0]-base})
    ROOT.mkdir(parents=True)
    save(ROOT/'source_contract.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'ARM9_sha256':sha(arm),'targets':targets,'interpreter_table':table,'core_sha256':CORE_SHA,
        'source_original_contact_and_shot_span':[0x020732FC,0x02074010],
        'no_ROM_instruction_or_emulated_state_patch':True,'full_goal_complete':False})
    def grouped(cpu,header,callback,original,selected,address):
        group=[t for t in targets if t['instruction_index']==selected[0]['instruction_index']]
        return assemble(cpu,header,callback,original,group,address)
    run=FunctionType(checker.main.__code__,{**checker.__dict__,'ROOT':ROOT,'assemble':grouped},argdefs=checker.main.__defaults__)
    run();controls=read(ROOT/'native_prefix_controls.json')
    assert len(controls['native_host_cases'])==30 and all(r['host_registers_flags_stack_CPU_prefix_original_return_and_one_original_call_exact']for r in controls['native_host_cases'])
    save(ROOT/'preflight.json',{'six_original_shot_boundaries':targets,'all30_grouped_prefix_ABI_controls_pass':True,
        'all8_main_RAM_mirror_controls_pass':len(controls['read_policy_cases'])==8,
        'no_gameplay_or_shot_outcome_claim':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Six original shot boundaries,30 grouped host-register/flags/stack controls andeight RAM-read controls pass.',flush=True)
