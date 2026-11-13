"""Reconstruct approved B198 and reject semantic errors before the sole ROM-image mutation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B198_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B198_references_v5746 import FLAGS,OUTPUT as DOC,MAP
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_atomic_v5754')
PARENT=Path('out/all_routes_combined_v5692_candidate.nds')
SEAL=Path('work/analysis/lil_B198_reference_approval_v5746/reference_approval.json')
NATIVE=Path('work/analysis/lil_B198_native_approval_v5724/all17_source_prose_current_native_approval.json')
if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    verified=read('work/analysis/editorial_handoff_verification_v5751/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert sha(PARENT.read_bytes())==verified['candidate_sha256']
    doc,mapping=read(DOC),read(MAP);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    deps={str(DOC),str(MAP),str(SEAL),str(NATIVE),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B198_layout_v2.py','dk4tool/dialogue/lil_B198_profile.py','dk4tool/dialogue/layout.py',
        'dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md'}
    deps.update(doc[k[:-7]] for k in doc if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file())
    deps.update(mapping[k] for k in ['source_plan','source_census']);deps.update(mapping['evidence'])
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py',
        'translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',
        *[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        value=read(p)
        if not isinstance(value,dict):continue
        for key in ['evidence','dependencies']:
            for item in value.get(key,{}) if isinstance(value.get(key),dict) else []:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    deps={p for p in deps if Path(p).resolve() not in excluded}
    conf=dict(format='dk4-lil-B198-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),reference_approval=str(SEAL),native_approval=str(NATIVE),
        required_map_flags=FLAGS,required_term_flags=owned.TERM_FLAGS,
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,config)
    assert test.read_file(owned.PATH)==Path(read(mapping['source_plan'])['target_SC2']).read_bytes() and len(proof['changed_records'])==17
    assert all(test.read_file(p)==v for _,p,v in parent.iter_files() if p!=owned.PATH) and all(test.read_file(p)==v for p,v in parent.iter_components())
    save(ROOT/'positive_reconstruction.json',proof)
    original_load=owned.load;negatives=[]
    def reject(label,path,edit):
        image=NdsImage.open(PARENT);value=deepcopy(read(path));before=deepcopy(value);edit(value);assert value!=before,label
        initial=[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']];calls=[];replace=image.replace_file
        image.replace_file=lambda *a,**k:(calls.append((a,k)),replace(*a,**k))[1]
        owned.load=lambda p:deepcopy(value) if Path(p)==Path(path) else original_load(p)
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError) as exc:reason=str(exc) or type(exc).__name__
            else:raise RuntimeError('Negative accepted:'+label)
        finally:owned.load=original_load
        assert not calls and initial==[image.read_file(p) for p in [owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4']],label
        negatives.append(dict(label=label,rejected=True,reason=reason,sole_mutation_not_reached=True))
        if len(negatives)%10==0:print('Semantic negatives passed:'+str(len(negatives)),flush=True)
    mutations=[]
    for key in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256']:
        mutations.append(('wrong-'+key,str(config),lambda v,k=key:v.update({k:'0'*64})))
    mutations += [
        ('lost-map-requirement',str(config),lambda v:v['required_map_flags'].pop()),
        ('lost-source-context-requirement',str(config),lambda v:v['required_term_flags'].pop()),
        ('missing-speech',str(DOC),lambda v:v['records'].pop()),
        ('wrong-policy',str(DOC),lambda v:v.update(translation_policy='natural-dialogue-v1')),
        ('wrong-locale',str(DOC),lambda v:v.update(target_locale='en-GB')),
        ('unchecked-format',str(DOC),lambda v:v.update(formatting_review_pending=True)),
        ('lost-retention-reason',str(DOC),lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
        ('invented-prose',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}Hello, sister.')),
        ('wrong-selector',str(DOC),lambda v:v['records'][0].update(source_selector=2)),
        ('wrong-full-preamble',str(DOC),lambda v:v['records'][0].update(source_complete_preamble_hex='0040ffff0002')),
        ('wrong-source-index',str(DOC),lambda v:v['records'][0].update(source_record_index=4)),
        ('wrong-current-index',str(DOC),lambda v:v['records'][0].update(current_record_index=4)),
        ('wrong-source-reference',str(DOC),lambda v:v['records'][0]['source_reference'].update(offset=14)),
        ('wrong-current-reference',str(DOC),lambda v:v['records'][0]['current_reference'].update(offset=14)),
        ('invented-FI',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}{MACRO:FI} was naughty.')),
        ('weak-wrap-waiver-transferred',str(DOC),lambda v:v['records'][0].update(qa_waivers=['weak-line-ending'],qa_waiver_reason='copy')),
        ('offline-conditional-claimed-gameplay',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==65).update(actual_B22_display_fixture_observed=True)),
        ('actual-pause-claimed-offline',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==49).update(actual_B22_display_fixture_observed=False)),
        ('missing-command-map-entry',str(MAP),lambda v:v['blocks'][0]['command_map'].pop()),
        ('missing-independent-map-entry',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
        ('wrong-nested-ancestor',str(MAP),lambda v:next(c for c in v['blocks'][0]['mapped_native_commands'] if c['source_0100_ancestors'])['target_0100_ancestors'].append(8)),
        ('missing-relative-site',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'].pop()),
        ('wrong-relative-target',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=146)),
        ('wrong-relative-unmatched',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_unmatched_next=142)),
        ('wrong-relative-source-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(source_span=6)),
        ('wrong-relative-target-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(target_span=6)),
        ('missing-target-skip-proof',str(MAP),lambda v:v['blocks'][0]['target_native_skip_cases'].pop()),
        ('wrong-source-logical-extent',str(MAP),lambda v:v['blocks'][0].update(source_logical_end=546)),
        ('wrong-target-logical-extent',str(MAP),lambda v:v['blocks'][0].update(research_logical_end=642)),
        ('wrong-speech-record-index',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(new_record_index=6)),
        ('wrong-source-ending',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(source_offset=542)),
        ('wrong-target-ending',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=642)),
        ('missing-native-plane',doc['native_font_proof'],lambda v:v['cases'].pop()),
        ('clipped-native-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost-native-page',doc['native_font_proof'],lambda v:v['cases'][0].update(one_native_page_consumes_complete_target=False)),
        ('missing-native-negative',doc['native_font_proof'],lambda v:v['negative_controls'].pop()),
        ('wrong-native-style',doc['native_font_proof'],lambda v:v.update(source_original_progressive_caller_style=1)),
        ('wrong-stored-style',doc['final_padding_proof'],lambda v:v.update(source_original_progressive_caller_style=1)),
        ('lost-stored-alignment',doc['final_padding_proof'],lambda v:v.update(current_final_stored_macro_alignment_cases=64)),
        ('lost-final-native-plane',doc['final_padding_proof'],lambda v:v.update(all17_final_targets_complete_native_planes_equal_reviewed_planes=False)),
        ('missing-relocated-predicate',doc['relocated_control_proof'],lambda v:v['original_unforced_predicate_pairs'].pop()),
        ('missing-relocated-picture',doc['relocated_control_proof'],lambda v:v['original4835_picture_pair'].pop()),
        ('wrong-actor-dispatch',doc['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][0].update(resolved_actor_ID=2)),
        ('missing-control-leaf',doc['relocated_control_proof'],lambda v:v['all12_source_current_target_control_leaves'].pop()),
        ('missing-end-probe',doc['termination_decode_proof'],lambda v:v['cases'].pop()),
        ('wrong-source-style-field',doc['source_original_progressive_style_proof'],lambda v:v.update(source_context_style_field=0x34)),
        ('wrong-source-style11',doc['source_original_progressive_style_proof'],lambda v:v.update(source_explicit_style=1)),
        ('lost-pause-style-ink-match',doc['source_original_progressive_style_proof'],lambda v:v['cases'][0].update(exact_actual_ink=False)),
        ('lost-pause-style-gray-match',doc['source_original_progressive_style_proof'],lambda v:v['cases'][0].update(exact_actual_gray=False)),
        ('missing-ASCII-style-control',doc['source_original_progressive_style_proof'],lambda v:v['cases'].pop()),
        ('lost-actual-style-binding',doc['representative_proof'],lambda v:v.update(source_story_style11_binds_complete_CP932_pause_planes_without_ROM_change=False)),
        ('missing-actual-panel',a:=read(doc['postscene_native_state_proof'])['actual_proof'],lambda v:v['actual_panels'].pop()),
        ('wrong-measured-holds',a,lambda v:v.update(complete_matching_holds=55)),
        ('wrong-actual-conditional-scope',a,lambda v:v.update(offline_only_source_indices=[])),
        ('wrong-measured-command-result',a,lambda v:v['versions'][1]['command_pairs'][-1].update(native_result=[3,0])),
        ('wrong-measured-inputs',a,lambda v:v['versions'][1].update(input_schedule_sha256='0'*64)),
        ('lost-actual-conditional-label',a,lambda v:v['versions'][1]['selected_intervals'][0].update(source_record_index=65)),
        ('lost-postscene-limit',doc['postscene_native_state_proof'],lambda v:v.update(no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim=False)),
        ('missing-viewed-screen',doc['postscene_native_state_proof'],lambda v:v['all_actual_consumer_sheets_viewed'].pop()),
        ('lost-viewed-status',doc['postscene_native_state_proof'],lambda v:v['paired_full_screen_views'][0].update(viewed_in_full_current_turn=False)),
        ('wrong-refrain-phrase',doc['source_bound_wrap_retention_proof'],lambda v:v.update(phrase_protection=['any','here'])),
        ('wrong-refrain-source-indices',doc['source_bound_wrap_retention_proof'],lambda v:v.update(exact_source_indices=[10])),
        ('invented-dramatic-break',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:FE}Any naughty children here?{LB}Any naughty children here?')),
        ('wrong-prose-name',doc['actor_terminology_reconciliation'],lambda v:v['approved_prose_names'].update({'12':'Rafael'})),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:v['fresh2_actor_names']['rows'][0].update(original_voice_class=0)),
        ('wrong-catalogue-name',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'12':'Yukihisa Shiraki'})),
        ('wrong-progressive-name',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'15':'Rafael'})),
        ('lost-reference-approval',str(SEAL),lambda v:v.update(all17_source_native_reference_and_representative_rules_approved=False))]
    for flag in FLAGS:mutations.append(('lost-map-'+flag,str(MAP),lambda v,k=flag:v.update({k:False})))
    for flag in owned.TERM_FLAGS:mutations.append(('lost-source-context-'+flag,doc['actor_terminology_reconciliation'],lambda v,k=flag:v.update({k:False})))
    for label,path,edit in mutations:reject(label,path,edit)
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,
        semantic_load_overrides_leave_real_hashes_intact_to_exercise_guards=True,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'atomic_validation_receipt.json',dict(positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),
        negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,
        config=str(config),config_sha256=sha(config.read_bytes()),parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=17,
        dependencies=len(conf['dependencies']),new_ROMs=0,new_review_credit=0,full_goal_complete=False))
    print(dict(positive_records=17,semantic_negatives=len(negatives),dependencies=len(conf['dependencies']),all_before_mutation=True))
