"""Current six-mode native eligibility and target lists on explicit CPU-only qualifications."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_letter_eligibility_v790 as original
from scripts.verify_letter_eligibility_v790 import menu
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/letter_predicates_v2239')
ROM=Path('out/all_routes_combined_v2171_candidate.nds')
ARM='ab7475ec929bd271c54f8b88cdb2fb10fd71ceb5f54b988507d073f0e3466bde'
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');assert sha(arm)==ARM
    snap=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];raw=Path(snap['path']).read_bytes();assert sha(raw)==snap['sha256']and len(raw)==0x400000
    qualified,proof=FunctionType(original.set_condition.__code__,{**original.__dict__,'ARMS':{ARM}})(arm,raw,{'mode':'Istanbul-letter-eligibility'})
    assert proof['all_other4MiB_bytes_exact']and len(proof['changes'])<=9
    cases=[]
    flags=menu(arm,qualified);assert flags==[1]*6
    cases.append(dict(case='original native Speech215 and source targets',flags=flags))
    for speech in(79,80,99,100,119,120,199,200):
        flags=menu(arm,qualified,speech);assert flags==[1,int(speech>=80),int(speech>=100),int(speech>=120),1,int(speech>=200)]
        cases.append(dict(case='source Speech-getter scalar boundary only',Speech=speech,flags=flags))
    cpu,get=get_machine(arm,qualified);item=get(0xCB190)+4+149*20
    missing=bytearray(qualified);missing[item+17-0x02000000]&=~4
    flags=menu(arm,bytes(missing),200);assert flags==[1,1,1,1,1,0]
    cases.append(dict(case='Speech200 without source regional proof acquired bit',flags=flags))
    flags=menu(arm,raw);assert flags==[1,0,0,0,0,0]
    cases.append(dict(case='unmodified no First Mate;outer Guild entry separately disabled',flags=flags))
    targets=proof['all_six_original_target_filters'];assert len(targets)==6 and all(2 not in r['faction_IDs']for r in targets)
    # Determine the exact mutable own-company name pointer through its original virtual getter.
    root=get(0xCB160);own=get(0x397D8,root);assert own==2
    obj=root+4+own*76
    import struct
    vt=struct.unpack('<I',cpu.mem_read(obj,4))[0];fn=struct.unpack('<I',cpu.mem_read(vt+8,4))[0]
    name=get(fn-0x02000000,obj);old_name=bytes(cpu.mem_read(name,128)).split(bytes(1))[0]
    assert len(old_name)<=18
    renamed=bytearray(qualified);renamed[name-0x02000000:name-0x02000000+19]=b'ABCDEFGHIJKLMNOPQR'+bytes(1)
    renamed_cpu,renamed_get=get_machine(arm,bytes(renamed));renamed_lists=[]
    for mode in range(6):
        count=renamed_get(0x5BB4C,0,mode,0x02470000)
        ids=list(struct.unpack('<'+'I'*count,renamed_cpu.mem_read(0x02470000,count*4)))if count else[]
        assert ids==targets[mode]['faction_IDs']and own not in ids
        renamed_lists.append(dict(type=mode,faction_IDs=ids))
    save(ROOT/'current_six_mode_eligibility_and_name_input_contract.json',dict(current_ROM=str(ROM),current_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),source_snapshot=snap,explicit_CPU_only_qualification=proof,all11_current_original_menu_predicate_cases=cases,all_six_current_original_target_lists=targets,original_mutable_own_company_name_pointer=name,source_name_hex=old_name.hex(),supplied18_byte_own_name='ABCDEFGHIJKLMNOPQR',six_target_lists_after_CPU_only_name_change=renamed_lists,own_editable_company_excluded_from_all_six_lists=True,no_target_or_menu_flag_override=True,positive_cases_use_original_real_native_Speech_and_proof_getters=True,boundary_cases_stub_only_declared_Speech_scalar=True,qualifications_and_name_are_CPU_test_inputs_not_emulator_fixtures_or_earned_states=True,original_source_producer=str(Path(original.__file__)),original_source_producer_sha256=sha(Path(original.__file__).read_bytes()),no_ROM_or_live_save_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(current_predicate_cases=len(cases),target_lists=6,own_edited_name_excluded=True,CPU_only=True),flush=True)
