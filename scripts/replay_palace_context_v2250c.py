"""Bind Palace6 context explicitly in the shared preinteraction CPU snapshot."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/palace_context_v2250c');OLD=Path('scripts/context_palace_v795.py')
if __name__=='__main__':
    assert not ROOT.exists();snapshot=read('work/analysis/item_context_v2235/native_context.json')['pre_fixture_snapshot'];assert sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
    source=OLD.read_text()
    changes={'work/analysis/palace_editorial_v795':'work/analysis/palace_context_v2250c','out/all_routes_combined_v792_candidate.nds':'out/all_routes_combined_v2171_candidate.nds','E:/Rota Nova translations/Generated/work/emulation_v193/palace_v794_context/frame_004800_arm9_ram.bin':Path(snapshot['path']).as_posix()}
    for old,new in changes.items():assert source.count(old)==1;source=source.replace(old,new)
    old='raw=RAM.read_bytes();cpu=machine(arm);cpu.mem_write(BASE,raw)'
    new=old+'''
    global_pointer=struct.unpack_from('<I',arm,0x5DC90)[0]
    facility=struct.unpack('<I',cpu.mem_read(global_pointer,4))[0]+0x10
    before=bytes(cpu.mem_read(BASE,0x800000));facility_before=struct.unpack('<I',cpu.mem_read(facility,4))[0]
    cpu.mem_write(facility,struct.pack('<I',6));after=bytearray(cpu.mem_read(BASE,0x800000));after[facility-BASE:facility-BASE+4]=before[facility-BASE:facility-BASE+4]
    assert bytes(after)==before
    save(ROOT/'CPU_facility_context.json',dict(field=facility,before=facility_before,after=6,only_four_bytes_in8MiB_changed=True,not_an_emulator_fixture_or_actual_Palace_visit=True))
'''
    assert source.count(old)==1;source=source.replace(old,new)
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
    save(ROOT/'current_replay_provenance.json',dict(original=str(OLD),original_sha256=sha(OLD.read_bytes()),effective_source_sha256=sha(source.encode()),current_genuine_preinteraction_snapshot=snapshot,CPU_facility_role6_letter_flag_and_numeric_inputs_not_earned_or_actual_events=True,all31_original_consumers_and218_monthly_providers_replayed=True,no_ROM_or_runtime_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
