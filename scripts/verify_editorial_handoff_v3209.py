"""Independent 235-object completion, exact release and fresh startup audit."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch import lil_shrines_temples_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_handoff_verification_v3209')
CHECKPOINT=Path('work/analysis/lil_Shrines_Temples_completion_v3208')
REG=Path('work/analysis/lil_Shrines_Temples_registration_v3203b')

if __name__=='__main__':
    assert not ROOT.exists()
    rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)
    for group in ['evidence','updated_files']:
        for p,digest in receipt[group].items():assert sha(Path(p).read_bytes())==digest,(group,p)
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp)
    backup=CHECKPOINT/'editorial_review_current_v1.json.before';before=read(backup)
    oldproof=read(receipt['prior_verified_handoff'])
    assert sha(backup.read_bytes())==oldproof['ledger_sha256']
    assert sha(Path(oldproof['handoff_receipt']).read_bytes())==oldproof['handoff_receipt_sha256']
    for p,digest in read(oldproof['handoff_receipt'])['updated_files'].items():
        saved=CHECKPOINT/(Path(p).name+'.before')
        assert sha((saved if saved.exists() else Path(p)).read_bytes())==digest
    fresh,oldfresh=ledger['contextual_story_natural_dialogue_pass_v1871'],before['contextual_story_natural_dialogue_pass_v1871']
    final=read(fresh['latest_final_review']);rows=final['records'];selected={historical_key(r) for r in rows}
    assert len(rows)==len(selected)==235 and Counter(r['editorial_decision'] for r in rows)=={'revise':117,'retain-wording':118}
    assert all(all(r['review'].values()) and r['source_meaning'] and r['localization_note']
        and r['all_source_native_representative_and_registered_gates_pass'] for r in rows)
    keys={historical_key(r) for r in fresh['record_keys']};integrated={historical_key(r) for r in fresh['integrated_record_keys']}
    complete={historical_key(r) for g in ledger['completed_editorial_families'] for r in g['records']}
    oldcomplete={historical_key(r) for g in before['completed_editorial_families'] for r in g['records']}
    assert keys==integrated==complete==oldcomplete|selected and not oldcomplete&selected
    assert keys=={historical_key(r) for r in oldfresh['record_keys']}
    assert len(keys)==len(fresh['record_keys'])==len(fresh['integrated_record_keys'])==4425
    assert fresh['pending_record_keys']==fresh['pending_contextual_families']==[] and fresh['latest_pending_contextual_family'] is None
    assert (fresh['fresh_pass_records_explicitly_reread'],fresh['fresh_pass_records_integrated'],fresh['fresh_pass_records_pending_native_actual_release'])==(4425,4425,0)
    assert Counter(p for p,k in keys)==ledger['completed_editorial_record_counts_by_file']=={
        '/COMMON/MESFILE.DK4':1599,'/data/SC2.DK4':2598,'/data/SC0.DK4':117,'/data/SC1.DK4':73,'/data/SC3.DK4':38}
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(4425,3040,1385)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==4428
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==before['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    assert not any(ledger['active_source_prose_drafts']['route_record_subsets_pending'].values())
    assert ledger['completed_editorial_families'][:-1]==before['completed_editorial_families']
    for k in ['unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal',
        'native_source_universe_inventory_v2701c','source_prose_reviewed_counts_by_file']:assert ledger[k]==before[k],k
    candidate=ledger['current_integrated_candidate'];path=Path(candidate['path']);image=NdsImage.open(path);clean=NdsImage.open('work/clean.nds')
    release=read('work/analysis/lil_Shrines_Temples_release_v3205/registered_release_verification.json')
    assert sha(path.read_bytes())==candidate['sha256']==release['candidate_sha256']==final['candidate_sha256']
    assert Path(release['exact_patch_reconstruction']).read_bytes()==path.read_bytes() and release['whole_ROM_reconstruction_byte_exact']
    for p,digest in [(candidate['patch'],candidate['patch_sha256']),(release['manifest'],release['manifest_sha256']),
        ('work/clean.nds',release['clean_input_sha256'])]:assert sha(Path(p).read_bytes())==digest
    manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    assert manifest['profile']==candidate['profile']=='all-routes-unified-v3204' and len(manifest['batches'])==515
    assert all(manifest['checks'].values()) and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    restored=deepcopy(registry);restored['profiles'].pop('all-routes-unified-v3204')
    assert restored==read(REG/'registry_before_raw.json')
    registration=read(REG/'registration_receipt.json')
    assert sha(Path('scripts/build_integrated_release.py').read_bytes())==registration['builder_sha256']
    assert sha((REG/'registry_before_raw.json').read_bytes())==read(before['current_integrated_candidate']['manifest'])['release_stack_sha256']
    parent=NdsImage.open(before['current_integrated_candidate']['path']);base=NdsImage.open(manifest['base_rom'])
    original_parent=NdsImage.open(before['current_integrated_candidate']['path'])
    result=owned.apply_release(parent,base)
    assert parent.read_file(owned.PATH)==image.read_file(owned.PATH) and result==release['stage']
    assert release['file_changes']==[owned.PATH] and release['component_changes']==[]
    assert release['all515_manifest_batches_and114_accepted_layers_present']
    assert sha(image.read_file('/__arm9__.bin'))==before['current_integrated_candidate']['ARM9_sha256']
    en,jp,old=[IlnkContainer.parse(im.read_file(owned.PATH)).blocks for im in [image,clean,original_parent]]
    assert [n for n,(a,b) in enumerate(zip(old,en,strict=True)) if a!=b]==list(range(101,111))
    doc=read(final['manuscript']);voice=read(final['actor_styles']);menu_doc=read(final['choices'])
    mapping=read(doc['reference_map'])
    assert sum(len(b['mapped_native_commands']) for b in mapping['blocks'])==421
    assert sum(len(b['relative_skip_fixups']) for b in mapping['blocks'])==114
    assert sum(len(b['target_native_skip_cases']) for b in mapping['blocks'])==570
    assert sum(len(b['actor_style_commands']) for b in mapping['blocks'])==8
    assert sum(len(b['choice_commands']) for b in mapping['blocks'])==5
    assert mapping['all21_relocated_predicate_pairs_preserve_source_operands_and_results']
    source_rows={r['id']:r for d in [doc,voice,menu_doc] for r in d['records']}
    assert set(source_rows)=={r['id'] for r in rows}
    for r in rows:
        b=r['block'];sr,cr=r['source_reference'],r['integrated_reference'];value=bytes.fromhex(r['integrated_hex'])
        original=source_rows[r['id']]
        assert jp[b][sr['offset']:sr['offset']+sr['bytes']]==bytes.fromhex(r['source_hex'])==bytes.fromhex(original['source_hex'])
        assert en[b][cr['offset']:cr['offset']+cr['bytes']]==value==bytes.fromhex(r['current_hex'])
        assert en[b][cr['offset']+cr['bytes']]==0 and r['current_reference']==cr
        assert cr['record_index']==en[b][:cr['offset']].count(b'\0')
        predecessor=r['historical_source_prose_predecessor_fields'];pr=predecessor['current_reference']
        assert old[b][pr['offset']:pr['offset']+pr['bytes']].hex()==predecessor['current_hex']==original['current_hex']
        assert r['english']==original['english'] and r['source_meaning']==original['source_meaning']
        if r['kind']=='typed-choice-label':
            assert value.decode('ascii')==r['english'];at=cr['command_offset'];i=r['option_index']
            assert en[b][at:at+2]==b'\0\x22' and at+8+struct.unpack_from('<H',en[b],at+2+2*i)[0]==cr['offset']
        elif r['kind']=='typed-4100-actor-style-alternative':
            at=cr['command_offset']
            assert en[b][at:at+2]==b'\0\x41' and en[b][at+18:at+20]==b'\0\xd0'
            assert r['compiled_hex']=='d0'+value.hex() and r['compiled_stored_alternative_hex']==value.hex()
            assert all(at+20+struct.unpack_from('<H',en[b],at+2+2*i)[0]==cr['offset'] for i in r['style_indices'])
            assert r['current_English']==value.decode('ascii')
        else:
            assert en[b][cr['offset']-5:cr['offset']]==bytes.fromhex('0040ffff00')
            assert value[:1]==bytes.fromhex(r['source_hex'])[:1]
        if r['editorial_decision']=='retain-wording':
            logical=r['english'] if r['kind']=='typed-choice-label' else r['english'].split('}',1)[1]
            assert logical==r['effective_predecessor_paragraph'] and r['fresh_retained_wording_justification']
    font=read(doc['native_font_proof']);padding=read(doc['final_padding_proof']);sample=read(doc['representative_proof'])
    assert len(font['cases'])==220 and font['current_original_macro_alignment_calls']==1760
    assert font['all220_current_native_planes_and_complete_glyphs_pass']
    assert len(font['source_bound_formatter_negatives'])==28 and len(font['source_English_macro_control_invariants'])==220
    assert len(font['all33_review_sheets'])==33
    for s in font['all33_review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert padding['current_final_padded_macro_alignment_cases']==880 and len(padding['final_target_parity_cases'])==220
    assert all(c['complete_final_target_native_plane_equals_reviewed_plane'] and c['tail_padding_consumed_without_blank_page_or_lost_glyph'] for c in padding['final_target_parity_cases'])
    assert sum(bool(r.get('qa_waivers')) for r in rows)==54 and all(r.get('qa_waivers') in [None,['line-break-count']] for r in rows)
    choices=read(doc['native_choice_proof']);fe=read(doc['native_FE_font_proof']);control=read(doc['relocated_control_proof'])
    assert choices['native_selection_cancel_cases']==40 and choices['complete_current_and_reviewed_style_label_planes']==60
    assert len(fe['cases'])==30 and fe['current_original_null_actor_macro_alignment_cases']==240
    assert fe['all30_one_native_page_consumes_complete_target'] and fe['two_source_staging_cases_start_English_firstline_with_complete_glyphs']
    assert len(control['relocated_dispatch_cases'])==220 and len(control['current_and_relocated_whole_original4100_command_cases'])==16
    assert len(control['all207_actor_style_current_and_relocated_pointer_cases']['cases'])==3312 and len(control['relocated_predicate_pairs'])==21
    assert control['original_event_queries']==[] and sample['no_open_translation_specific_display_or_control_finding']
    assert sample['actual_selected_Shrines_Temples_IDs']==sample['actual_three_option_menu_gameplay_coverage']==[]
    assert sample['new_emulator_runs']==0
    negatives=read(REG/'negative_cases.json')
    assert len(negatives['cases'])==44 and negatives['all_rejected_before_mutation']
    start=read('work/analysis/lil_Shrines_Temples_startup_v3207/cold_boot_Lil_startup_town_verification.json')
    assert start['candidate_sha256']==candidate['sha256'] and start['all_current_requested_and_final_framebuffers_equal_V3144']
    assert start['paired_frame_count']==31 and start['all_five_postload_actor_model_and_captain_checks_equal']
    assert start['current_Lil_captain2_and_B22_payload_verified'] and start['source_and_disposable_town_donor_unchanged']
    assert start['actual_selected_Shrines_Temples_IDs']==[]
    assert [(r['case'],r['frames']) for r in start['runs']]==[('newgame',4001),('town',17401)]
    for run in start['runs']:
        for key in ['report','old_report','plan','terminal']:assert sha(Path(run[key]).read_bytes())==run[key+'_sha256']
    review=read(CHECKPOINT/'current_six_frame_visual_review.json')
    assert review['viewed'] and review['sha256']==start['review_sheet_sha256']==sha(Path(review['sheet']).read_bytes())
    inventory=read(ledger['unfinished_editorial_scope_v3208']['path'])
    assert inventory['incomplete_COMMON_count']==3 and inventory['incomplete_route_source_prose_count']==0
    assert inventory['lil_shrines_scope_reconciled_v3208']['remaining_B111_B119']==182
    unit=next(u for u in ledger['coverage_units'] if u['id']=='all-route-scenes')
    assert (unit['reviewed_route_records'],unit['completed_route_records'])==(2826,2826)
    assert ledger['raw_source_coverage_revisit']['status']=='open-before-whole-goal-completion'
    assert ledger['next_named_target_reports_source_lead_v2664']['completion_credit_added']==0
    assert Path('docs/editorial_handoff_current.md').read_text(encoding='utf-8').startswith('# Current editorial handoff - V3208')
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete']
    assert read('work/analysis/lil_Shrines_Temples_build_v3204/build_terminal.json')['returncode']==0
    ROOT.mkdir(parents=True)
    save(ROOT/'verified_handoff.json',dict(checkpoint='V3208',ledger=str(lp),ledger_sha256=sha(lp.read_bytes()),
        handoff_receipt=str(rp),handoff_receipt_sha256=sha(rp.read_bytes()),fresh_records=4425,fresh_integrated=4425,fresh_pending=0,
        source_prose=4428,new_source_prose_reviews=0,new_completed_records=235,revisions=117,justified_retentions=118,
        completed_records=4425,historical_revised=3040,historical_retained=1385,incomplete_COMMON=3,incomplete_route=0,
        source_native_reference_representative_registered_release_and_current_startup_all_bound=True,
        all235_exact_clean_predecessor_effective_and_integrated_references_verified=True,
        all33_native_sheets_and_current6frame_sheet_reviewed=True,narrow_line_count_notes=54,
        actual_selected_Shrines_Temples_IDs=[],actual_three_option_menu_gameplay_coverage=[],
        new_current_candidate_emulator_runs=2,paired_current_whole_framebuffers=31,
        candidate=candidate['path'],candidate_sha256=candidate['sha256'],patch=candidate['patch'],patch_sha256=candidate['patch_sha256'],
        manifest_batches=515,accepted_layers=114,whole_clean_input_patch_reconstruction_exact=True,
        prior_ROMs_profiles_translation_and_V1492_promotion_preserved=True,legacy_console_count_literals_not_used_as_evidence=True,
        prior_ledger_and_updated_file_chains_verified=True,all_jobs_terminal=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('IndependentV3208audit passes:235completed inV3204;4425reread/integrated,4428source-prose;515batches/114layers/exactpatch/31currentframepairs. Remaining182andfullwidergoal stayopen.')
