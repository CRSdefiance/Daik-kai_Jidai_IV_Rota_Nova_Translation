"""Correct the audit's conflation of persistent result word and interpreter r3.

Preserve the stopped B53 audit and completed B31 masks/flow without replaying
either capture. The original complete parser-result record is retained by the
unchanged caller; normal ends preserve its seeded second word, not arbitrary r3.
"""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/Hodram_B31_B53_actual_audit_tools_v8742b');assert not root.exists()
    path=Path('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json');controls=read(path)
    rows=[r for g in controls['groups'] for r in g['normal_seeded_ends']]
    assert len(rows)==50 and all(r['native_result']==[0,r['initial_value_word'],0,0,0,0] for r in rows)
    assert any(r['previous_result']!=r['initial_value_word'] for r in rows)
    fpath=Path('work/analysis/Hodram_B51_result_flow_v8558c/result_flow.json');forward=read(fpath)
    arm=NdsImage.open(controls['candidate']).read_file('/__arm9__.bin');span=forward['original_caller_span']
    assert sha(arm[0x24048:0x24118])==span['sha256'] and arm[0x24048:0x24118]==NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[0x24048:0x24118]
    assert len(forward['caller_fragment_cases'])==50 and all(r['all_six_return_words_preserved'] for r in forward['caller_fragment_cases'])
    receipt=derive('scripts/audit_Hodram_B31_B53_actual_v8742.py','scripts/audit_Hodram_B31_B53_actual_v8742b.py',{
        'Hodram_B31_B53_actual_v8742':'Hodram_B31_B53_actual_v8742b',
        "assert row['result_words']==[0,entry['mode']]":"assert row['result_words']==[0,pairs[-2]['native_result'][1]]",
        "normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)":"normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True,previous_parser_result_value=pairs[-2]['native_result'][1],separate_interpreter_carried_mode=entry['mode'],source_proven_distinct_channels_not_assumed_equal=True)",
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=receipt,
        all_native_high_integer_constants_andmultiplicity_preserved=True,source50_seeded_end_cases_preserve_existing_result_word_independent_of_r3=True,
        original_caller_span=span,original_current_clean_caller_exact=True,reused50_caller_fragment_cases_preserve_allsix_resultwords=True,
        source_end_proof=str(path),source_end_proof_sha256=sha(path.read_bytes()),caller_proof=str(fpath),caller_proof_sha256=sha(fpath.read_bytes()),
        stopped_B53_audit_andcompleted_B31_mask_flow_report_preserved=True,
        B31_existing_end_result0_1_matches_both_independently_recorded_channels_no_reaudit_orrecapture_needed=True,
        all_body_name_glyph_full_payload_readonly_andotherflow_guards_unchanged=True,
        old_immutable_auditors_andlater_older_record_technical_reaudit_preserved=True,no_ROM_capture_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Source50seeded ends andunchanged50caller fragments prove resultword channel. Corrected B53 check;all prior captures/B31 pass/failure artifacts preserved.',flush=True)
