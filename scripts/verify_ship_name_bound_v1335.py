"""Bind the actual ship-rename editor to its original eighteen-byte child cap.

CPU-only append probes stop after original bounded copy/NUL, before redraw.
They do not rename a live ship or claim complete keyboard/hardware testing.
"""
import struct
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.probe_button_prompt_native import STACK,STOP
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_name_bound_v1335')
REPORT = Path('work/emulation_v193/refit_dialogue_v832_name_entry/capture_report.json')
BASE = 0x02000000


def main():
    assert not ROOT.exists()
    report = read(REPORT)
    assert report['frames']==14600 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['ROM_sha256']=='3d6f3d28deedb42f9d5c333fd5a70b0722438f04e76a089b84672c2299c84d95'
    snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==13700)
    raw_path = Path(snapshot['path'])
    raw = raw_path.read_bytes()
    assert sha(raw)==snapshot['sha256'] and len(raw)==0x400000
    parents = []
    for o in range(0,len(raw)-0xDC,4):
        if [struct.unpack_from('<I',raw,o+n)[0] for n in [0,4,0x38]]==[0x021558CC,0x0215591C,0x02155D44]:
            parents.append(BASE+o)
    assert parents==[0x0218E2C0]
    parent = parents[0]
    assert raw[parent-BASE+0xB4:parent-BASE+0xD8].split(b'\0')[0]==b'Vestaros'
    assert struct.unpack_from('<I',raw,parent-BASE+0xD8)[0]==18
    arm = NdsImage.open('out/all_routes_combined_v1316_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    spans = []
    for lo,hi in [(0xB08C8,0xB0A18),(0xAFD4C,0xAFDB4),(0xCED28,0xCED50)]:
        assert arm[lo:hi]==clean[lo:hi]==raw[lo:hi]
        spans.append({'span':[BASE+lo,BASE+hi],'sha256':sha(arm[lo:hi]),
            'instructions':[{'address':i.address,'mnemonic':i.mnemonic,'operands':i.op_str} for i in md.disasm(clean[lo:hi],BASE+lo)]})
    assert struct.unpack_from('<I',clean,0xB08D4)[0]==0x020CED28
    cpu,get = get_machine(arm,raw)
    assert get(0xB08C8,parent+0x38)==8
    cases = []
    for text in [b'F',b'F'*17,b'F'*18,b'F'*19,'長崎丸'.encode('cp932'),'長崎丸長崎丸長崎丸'.encode('cp932')]:
        cpu,get = get_machine(arm,raw)
        cpu.mem_write(parent+0xB4,b'\0'*36)
        pointer = 0x02470000
        cpu.mem_write(pointer,text+b'\0')
        # This is an explicit original post-copy/pre-redraw boundary,not a
        # fabricated successful method return or a replacement capacity check.
        hook = cpu.hook_add(UC_HOOK_CODE,lambda u,p,s,d:u.emu_stop(),begin=BASE+0xB0950,end=BASE+0xB0950)
        cpu.reg_write(UC_ARM_REG_SP,STACK)
        cpu.reg_write(UC_ARM_REG_LR,STOP)
        cpu.reg_write(UC_ARM_REG_R0,parent+0x38)
        cpu.reg_write(UC_ARM_REG_R1,pointer)
        cpu.emu_start(BASE+0xB08D8,STOP,count=100000)
        assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0xB0950
        cpu.hook_del(hook)
        value = bytes(cpu.mem_read(parent+0xB4,36)).split(b'\0')[0]
        assert value==text[:18] and get(0xB08C8,parent+0x38)==len(value)
        cases.append({'input_hex':text.hex(),'original_bounded_output_hex':value.hex(),'original_strlen_bytes':len(value),
            'stopped_before_original_redraw_not_full_method_ABI_or_live_name_edit':True})
    ROOT.mkdir(parents=True)
    save(ROOT/'original_ship_rename_capacity.json',{'source_report':str(REPORT),'source_report_sha256':sha(REPORT.read_bytes()),
        'snapshot':str(raw_path),'snapshot_sha256':sha(raw),'actual_ship_rename_keyboard_frame':13700,
        'actual_parent':parent,'parent_child_provider_vtables':[0x021558CC,0x0215591C,0x02155D44],
        'native_capacity_field':parent+0xD8,'max_name_bytes_excluding_NUL':18,
        'original_child_count_B08C8_tailcalls_CED28_strlen_not_character_count':True,
        'unchanged_clean_current_captured_code_spans':spans,'bounded_copy_cases':cases,
        'ASCII_length23_and31_prior_cases_are_extra_stress_not_legal_editor_names':True,
        'does_not_certify_other_editors_legacy_saves_or_all_keyboard_input_pages':True,
        'no_ROM_crew_RNG_or_live_game_state_changed':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Actual ship-rename editor cap18 bytes:original strlen and six bounded-copy probes pass;23/31-byte names are extra stress only.',flush=True)


if __name__=='__main__':
    main()
