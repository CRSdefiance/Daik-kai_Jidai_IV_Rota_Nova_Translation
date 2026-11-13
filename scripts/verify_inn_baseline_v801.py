"""Bind completed Inn cold-boot captures and research owned time-prefix strings."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch import palace_label_boundaries as current
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE
from scripts.verify_palace_gameplay_v797 import load
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/inn_context_v801')


def main():
    report_path,report,frames,ram=load('inn_v801_context',8600)
    assert report['ROM_sha256']=='f855781b6b2a23482874a81c4d3f8f77262fe7f7db2846399b1409da8cc67c79'
    rom=NdsImage.open(report['ROM']);arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    entries=current.current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    owner=struct.unpack_from('<I',arm,0x552A0)[0]
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    actual=[]
    for frame,number in ((4800,1177),(5200,1178),(6200,1179),(7000,1180),(7400,1181)):
        assert cstring(ram[frame],owner+0x2030)==entries[number].text
        actual.append(dict(frame=frame,message_id=number,capture=frames[frame],
            native_template_hex=entries[number].text.hex(),
            native_wrapped_hex=cstring(ram[frame],wrapped).hex(),
            scope='Current pre-revision text,exact active message cache and manually inspected actual framebuffer;not revised English verification.'))
    states=[]
    for frame in (4400,5600,8200,8600):
        u=machine(arm);u.mem_write(BASE,ram[frame])
        def get(fn,args=()):
            call(u,fn,args);return u.reg_read(UC_ARM_REG_R0)
        root=get(0xCB160);company=get(0x397D8,(root,))
        cash=get(0x3CCC8,(root+4+company*76,))
        cal=get(0xCB1B4);tick=struct.unpack('<I',u.mem_read(cal+8,4))[0]
        states.append(dict(frame=frame,company_ID=company,cash=cash,calendar_tick=tick))
    assert [s['cash'] for s in states]==[8371,8370,8367,8367]
    assert states[1]['calendar_tick']-states[0]['calendar_tick']==48
    assert states[2]['calendar_tick']-states[1]['calendar_tick']==144
    assert states[3]['calendar_tick']==states[2]['calendar_tick']
    lo,hi=0x02143DCC,0x02143DF4
    refs=sorted(census(rom,[(lo,hi)],[]))
    expected=sorted(['absolute','section0',BASE+at,struct.unpack_from('<I',arm,at)[0],False]
        for at in (0x5CB2C,0x5CB30,0x5CB34,0x5CB38))
    assert refs==expected,refs
    pointers=[];blob=bytearray()
    for english in ('Last month','This month','%s months ago'):
        pointers.append(lo+len(blob));blob.extend(english.encode()+b'\0')
    assert len(blob)==36 and hi-lo==40
    blob.extend(bytes(hi-lo-len(blob)))
    assert arm[hi-BASE:hi-BASE+8]==b'Reclaim\0'
    source_phrases=[]
    for at in (0x5CB2C,0x5CB30,0x5CB34,0x5CB38):
        p=struct.unpack_from('<I',arm,at)[0]
        source_phrases.append(dict(pointer=p,japanese=clean[p-BASE:].split(b'\0')[0].decode('cp932'),
            current_English=arm[p-BASE:].split(b'\0')[0].decode('ascii')))
    save(ROOT/'baseline_and_time_ownership.json',dict(
        candidate=report['ROM'],candidate_sha256=report['ROM_sha256'],
        completed_report=str(report_path),completed_report_sha256=sha(report_path.read_bytes()),
        terminal_exec_session=30596,terminal_exit_code=0,cold_boot=True,savestate_loaded=False,
        donor_source_unchanged=True,battery=report['battery_save_preloaded'],callback_errors=[],
        actual_message_caches=actual,native_money_calendar_states=states,
        one_night_cost1_and_calendar48=True,three_night_cost3_and_calendar144=True,
        normal_inn_menu_return_frames=[5600,8200],normal_town_return_frame=8600,
        old_time_prefix_owned_span=[lo,hi],old_time_prefix_source_hex=clean[lo-BASE:hi-BASE].hex(),
        old_time_prefix_current_hex=arm[lo-BASE:hi-BASE].hex(),source_time_phrases=source_phrases,
        complete_current_reference_census=refs,no_unknown_incoming_time_prefix_references=True,
        proposed_full_English_blob_hex=bytes(blob).hex(),proposed_pointers=dict(last=pointers[0],this=pointers[1],months_ago=pointers[2]),
        proposed_deduplicate_two_identical_format_strings=True,
        next_Reclaim_allocation_preserved_in_plan=True,ROM_changed=False,
        revised_English_actual_testing_pending=True,full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Terminal baseline:five active Inn IDs;1+3 nights cost4/ticks192;normal town return. Four time-prefix references;full phrases fit owned40 bytes with duplicate format sharing.',flush=True)


if __name__=='__main__':main()
