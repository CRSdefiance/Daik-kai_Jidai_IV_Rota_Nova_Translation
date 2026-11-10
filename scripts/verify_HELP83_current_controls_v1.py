"""Bind observed A/B sail controls andB/A Auto Move cancellation;do not misname generic flag bits."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.probe_button_prompt_native import machine,call
from unicorn.arm_const import UC_ARM_REG_R0

ROOT=Path('work/analysis/HELP83_current_sail_controls_20261104')
if __name__=='__main__':
    out=ROOT/'control_binding_v1.json';assert not out.exists()
    plan_path=ROOT/'run_plan_v2.json';plan=load(plan_path);report_path=ROOT/'capture_v2/capture_report.json';report=load(report_path)
    assert report['ROM_sha256']==plan['ROM_sha256']==sha(Path(plan['ROM']).read_bytes()) and report['frames']==9101
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert sha(Path(plan['battery']).read_bytes())==plan['battery_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    earlier=load(ROOT/'capture_v1/capture_report.json');shots={r['frame']:r for r in report['frames_captured']}
    common=sorted({r['frame']for r in earlier['frames_captured']} & set(shots));assert len(common)==14
    assert all(r['PNG_sha256']==shots[r['frame']]['PNG_sha256']for r in earlier['frames_captured']if r['frame']in common)
    for s in shots.values():assert sha(Path(s['path']).read_bytes())==s['PNG_sha256']
    arm=NdsImage.open(plan['ROM']).read_file('/__arm9__.bin');town_path=Path('work/analysis/Town_HELP23_release_verified_20261104/registered_release_verification.json');town=load(town_path)
    current=NdsImage.open(town['candidate']);prior=NdsImage.open(plan['ROM'])
    dependencies=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']
    assert all(current.read_file(p)==prior.read_file(p)for p in dependencies)
    snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']};states=[]
    expected={7300:0,7400:0,8050:0,8250:1,8450:3,8650:3,8850:1,9050:0}
    for frame,value in expected.items():
        snapshot=snapshots[frame];raw=Path(snapshot['path']).read_bytes();assert len(raw)==4194304 and sha(raw)==snapshot['sha256']
        for lo,hi in [(0xcb1a8,0xcb1b4),(0x82c4c,0x82c64)]:assert arm[lo:hi]==raw[lo:hi]
        cpu=machine(arm);cpu.mem_write(0x02000000,raw);call(cpu,0xcb1a8,());fleet=cpu.reg_read(UC_ARM_REG_R0)
        assert 0x02000000<=fleet<0x023fd000
        flag_address=fleet+0x2094;flags=bytes(cpu.mem_read(flag_address,1))[0];assert flags==value
        call(cpu,0x82c4c,(fleet+0x2090,1));bit1=cpu.reg_read(UC_ARM_REG_R0);assert bit1==(flags&2)
        assert bytes(cpu.mem_read(0x02000000,len(raw)))==raw
        states.append(dict(frame=frame,flag_address=flag_address,observed_byte=flags,generic_bit1_getter=bit1,
          own_current_snapshot=snapshot,native_read_only_getters_no_RAM_change=True))
    # These two actual states refute the old automatic-flag interpretation.
    assert states[0]['generic_bit1_getter']==0 and next(r for r in states if r['frame']==8450)['generic_bit1_getter']==2
    save(out,dict(ROM=plan['ROM'],ROM_sha256=plan['ROM_sha256'],current_ARM9_sha256=sha(arm),
      capture_report=str(report_path),capture_report_sha256=sha(report_path.read_bytes()),run_plan=str(plan_path),run_plan_sha256=sha(plan_path.read_bytes()),
      whole_frame_common_prefix=common,all14_shared_frames_exact_to_initial_probe=True,observed_states=states,
      observed_inputs=dict(A_opens_sails=True,B_closes_sails=True,A_reopens_from_anchored_state=True,
        B_opens_Stop_Auto_Move_question=True,A_confirms_return_to_manual=True),
      source83_physical_mapping=dict(circle='A',cross='B',L1='L',R1='R'),
      direct_visual_reading=dict(frame7300='Auto Sail andB Stop Auto Move footer',frame7360='Stop automatic movement? B No/A Yes',
        frame7400='Manual Rotate/Menu/Inspect/B-A Sails footer',frame8450='Anchored icon',frame8650='Still anchored',frame8850='Sails reopened',frame9050='Sails opened further'),
      source84_X_cancel_current_Help_isincorrect=True,
      at_least_two_levels_of_sail_closing_andreopening_observed=True,
      generic_82C4C_is_a_bit_accessor_not_proof_of_Auto_Move_state=True,
      later_older_record_technical_reaudit_counterexample=dict(proof='work/analysis/auto_move_riga_v399/actual_auto_move_proof.json',
        field='final_native_original_automatic_flag_clear',reason='The same fleet+2090 bit1 getter iszero during observed Auto Sail7300 andnonzero whileanchored manually8450. Its return cannot establish automatic sailing. Actual footer/question/confirmation evidence remains independently valid;preserve the historical proof.'),
      verified_current_Town_runtime_resources_equal=dependencies,verified_current_Town_release=str(town_path),verified_current_Town_release_sha256=sha(town_path.read_bytes()),
      actual_inherited_Riga_battery_no_new_RAM_code_coordinate_orunlock_fixture=True,no_full_route_story_orhardware_claim=True,
      source_donor_unchanged=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Own current A opens/B closes/anchored A reopens,andB/A Auto Move cancellation observed;14 shared frames exact.Getter interpretation isolated forlater re-audit.')
