"""Bind next2000 controls to unchanged actual source illustration-pause evidence."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B122_original2000_waits_v3265')
SOURCE=Path('work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json')
PAUSES=Path('work/analysis/lil_opening_navigation_v1707b/illustration_pause_confirmations.json')
SCENE=Path('work/analysis/lil_opening_scene_v1708/complete_B22_actual_scene_proof.json')
OLDER=Path('work/analysis/opening_holds_v686/proof.json')

if __name__=='__main__':
    assert not ROOT.exists();source,pauses,scene,older=map(read,[SOURCE,PAUSES,SCENE,OLDER])
    current,historical=NdsImage.open(source['current_ROM']),NdsImage.open(scene['research_ROM'])
    assert sha(Path(source['current_ROM']).read_bytes())==source['current_ROM_sha256'] and sha(Path(scene['research_ROM']).read_bytes())==scene['research_ROM_sha256']
    arm,oldarm=current.read_file('/__arm9__.bin'),historical.read_file('/__arm9__.bin')
    assert scene['all49_revised_dialogues_individually_activated_with98_complete_pixel_exact_holds'] and scene['all90_original_command_entry_return_pairs_and_entire3292_byte_resident_source_verified']
    assert scene['original_illustration_pauses_confirmed_with_normal_A']==pauses
    spans=[(0x24134,0x241C4),(0x2A1D8,0x2A228),(0x54E44,0x55110),(0xD15C8,0xD15F0),(0xD457C,0xD46D4),(0xD4C90,0xD4D08)]
    for a,b in spans:assert arm[a:b]==oldarm[a:b]
    for span in older['source_exact_code_ranges']:
        a,b=span['begin'],span['end'];assert sha(arm[a:b])==span['sha256']
    blocks,oldblocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [current,historical]]
    assert blocks[22]==oldblocks[22] and sha(blocks[22])=='83efe3b52aa551baa5683c7a6709e0b42b490eafc2ce2ff89455632bc67cb825'
    changed=[p for _,p,v in historical.iter_files() if current.read_file(p)!=v]
    assert changed==['/COMMON/MESFILE.DK4','/data/SC0.DK4','/data/SC1.DK4','/data/SC2.DK4','/data/SC3.DK4']
    reviewed=[]
    assert len(pauses['pauses'])==3
    for p in pauses['pauses']:
        s=p['source'];assert (s['route'],s['block'],s['first_word'])==(2,22,0x2000) and s['whole_resident_payload_exact_ROM']
        actual=Path(s['actual_payload_file']).read_bytes();assert sha(actual)==s['actual_sha256']==s['registered_sha256']==sha(blocks[22]) and actual==blocks[22]
        at=s['instruction_offset'];assert actual[at:at+2]==bytes.fromhex('0020') and p['normal_A_acknowledges_original_non_text_illustration_pause']
        capture=Path(p['capture']);assert capture.exists()
        reviewed.append(dict(frame=p['frame'],source_instruction_offset=at,capture=str(capture),capture_sha256=sha(capture.read_bytes()),viewed=True,finding='Historical actual illustration above an intentionally blank lower text area, with the normal A prompt; source2000 is an intentional nontext hold.'))
    controls=source['nontext_2000_commands'];assert len(controls)==2 and [c['command_offset'] for c in controls]==[58,228]
    cases=0
    for c in controls:
        assert c['block']==122 and c['source_command']['whole_command_hex']==c['current_command']['whole_command_hex']=='0020'
        for v in c['versions']:
            for case in v['cases']:
                assert case['native_extent']==2 and case['native_result']==[3,0,0,0,0,0] and case['no_source_resident_text_payload']
                calls=case['original_UI_boundary_calls'];assert len(calls)==1 and calls[0]['address']==0x02054E44 and calls[0]['args'][:2]==[0,0] and calls[0]['original_caller_return']==0x0202A218
                assert case['full_UI_body_effects_display_and_input_behavior_not_executed'];cases+=1
    assert cases==40
    for p,k in [(older['source_report'],'source_report_sha256'),(older['current_report'],'current_report_sha256')]:assert sha(Path(p).read_bytes())==older[k]
    ROOT.mkdir(parents=True)
    evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,PAUSES,SCENE,OLDER,Path('scripts/navigate_lil_opening_v1707b.py'),Path('scripts/verify_lil_opening_scene_v1708.py'),Path('scripts/verify_opening_holds_v686.py'),Path('docs/editorial_testing_scope_v1870.md'),Path(__file__)]}
    save(ROOT/'original2000_actual_rule_and_current_source_binding.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],evidence=evidence,source_bound_code_spans=[dict(begin=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],historical_Lil_actual_source_pauses=reviewed,all3_historical_pause_captures_viewed=True,current_and_historical_B22_whole_block_exact=True,all_nontext_ROM_assets_and_fonts_exact_to_historical_actual_Lil_run=True,changed_historical_to_current_text_files=changed,source_2000_controls=controls,current_clean_decoder_cases_with_explicit_UI_boundary=40,
        original2000_is_two_byte_nontext_illustration_pause_with_normal_A_acknowledgment=True,
        current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence=True,
        no_source_resident_label_or_paragraph_to_translate=True,
        preserve_both_2000_commands_and_their_mapped_resume_boundaries=True,
        source_intentional_blank_illustration_hold_is_not_an_English_padding_page_waiver=True,
        full_native_UI_body_not_reexecuted=True,historical_actual_evidence_reused_under_user_policy=True,
        transfer_scope='Zero-argument source2000 nontext pause and normal A acknowledgment. COMMON and story files changed across the historical interval, so prose/FE/menu rendering and current source/target transitions retain their separate per-record native and release gates.',
        actual_selected_B122_B127_IDs=[],new_emulator_runs=0,new_source_scene_or_earned_Clifford_progress_claimed=False,
        failed_uninitialized_UI_probe_preserved=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('Two B122source2000 controls bind to3viewed actualLil illustration pauses andexact currentcode/assets;40decoder cases pass. Preserve intentional source waits;nonewscene gameplay orprosecredit.')
