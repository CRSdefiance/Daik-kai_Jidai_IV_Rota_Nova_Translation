"""Reuse observed Refit footer/A cycling with exact current native code and descriptor bindings."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T44_T80_clean_20261104')
if __name__=='__main__':
    binding=ROOT/'HELP51_native_controls_v1.json';output=ROOT/'whole_article_comparisons_v2.json'
    assert not binding.exists() and not output.exists()
    comparison_path=ROOT/'whole_article_comparisons_v1.json';doc=load(comparison_path)
    proof_path=Path('work/analysis/refit_spritsail_actual_verification_v2290c/actual_revised_help_caption_and_startup.json');prior=load(proof_path)
    report_path=Path(prior['actual_report']['report']);assert sha(report_path.read_bytes())==prior['actual_report']['sha256']
    report=load(report_path);assert report['cold_boot'] and not report['savestate_loaded']
    snap=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==14300)
    ram=Path(snap['path']).read_bytes();assert len(ram)==snap['bytes']==4194304 and sha(ram)==snap['sha256']
    image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin')
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    spans=[]
    for lo,hi,scope in [(0x10000,0x20000,'complete code window containing CDeckRemodelView and related refit routines'),
      (0x1323a0,0x132454,'CDeckRemodelView vtable and associated descriptor window'),
      (0x114b00,0x114c00,'original input/Undo descriptor window'),
      (0xc7000,0xca000,'shared native view/input code window'),
      (0xa8000,0xac000,'native equipment operations code window')]:
        assert ram[lo:hi]==arm[lo:hi]
        spans.append(dict(current_ARM9_offset=lo,bytes=hi-lo,sha256=sha(arm[lo:hi]),scope=scope,exact_to_historical_actual_RAM=True))
    frames=[]
    for n in [14000,14300]:
        shot=next(r for r in report['frames_captured'] if r['frame']==n)
        assert sha(Path(shot['path']).read_bytes())==shot['PNG_sha256'];frames.append(shot)
    assert dict(start=14001,duration=8,buttons=['A']) in report['scripted_input_schedule']
    sheet=Path(prior['review_sheet']);assert sha(sheet.read_bytes())==prior['review_sheet_sha256']
    assert arm[0x11b5ec:].split(b'\0')[0]==b'Undo'
    save(binding,dict(current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],current_ARM9_sha256=sha(arm),
      historical_actual_proof=str(proof_path),historical_actual_proof_sha256=sha(proof_path.read_bytes()),
      original_hashed_capture_report=str(report_path),original_hashed_capture_report_sha256=sha(report_path.read_bytes()),
      original_hashed_RAM=snap,source_owned_current_dependency_spans=spans,
      historical_actual_frames=frames,historical_readable_sheet=str(sheet),historical_readable_sheet_sha256=sha(sheet.read_bytes()),
      direct_visual_footer_reading='A Edit; X Finish; Y Undo; B Back',
      A_cycling_observed_between14000_and14300=True,X_Finish_bound_by_native_footer_andunchanged_code_not_a_new_physical_X_press=True,
      source51_symbol_mapping=dict(circle='A',triangle='X'),current_HELP_Y_execution_instruction_isincorrect=True,
      inherited_five_ship_Copenhagen_battery_not_earned_campaign_progress=True,
      no_new_gameplay_visit_orfull_historical_ROM_equality_claim=True,
      historical_ROM_file_not_required_hashed_RAM_andframes_preserved=True,
      scope='Localize original source51 controls against its observed native consumer; no runtime or gameplay edits.',
      new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    before=doc['records'][7];assert before['topic_id']==51 and not before['review']['localization']
    row={**before,'english':before['english'].replace('the selection button','A').replace('the execution button','X'),
      'finding':before['finding']+' Bound correction: native Refit footer shows A Edit/X Finish/Y Undo. Historical A input14001 cycles the selected bow fitting by14300. All corresponding current code/vtable/descriptor windows match the original hashed actual RAM; this reuses historical consumer evidence and does not claim a fresh X press.',
      'native_term_orcontrol_binding_pending':False,'native_control_binding':str(binding),'native_control_binding_sha256':sha(binding.read_bytes()),
      'review':{**before['review'],'localization':True}}
    row['localization_note']=row['finding'];doc['records']=[row if r['topic_id']==51 else r for r in doc['records']]
    assert all(doc['records'][i]==r for i,r in enumerate(load(comparison_path)['records']) if r['topic_id']!=51)
    doc.update(first_four_gates_passed=37,pending_localization_binding_topic_IDs=[],source51_provisional_generic_buttons_must_not_ship=False,
      source51_A_cycle_X_finish_Y_Undo_conflict_resolved=True,previous_comparison=str(comparison_path),previous_comparison_sha256=sha(comparison_path.read_bytes()),
      source51_control_binding=str(binding),source51_control_binding_sha256=sha(binding.read_bytes()),
      all_fifth_gates_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()))
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    save(output,doc)
    print('Source51 corrected toA cycling/X finish,using bound historical native evidence;37 four-gate passes,all display gates pending,no new credit.')
