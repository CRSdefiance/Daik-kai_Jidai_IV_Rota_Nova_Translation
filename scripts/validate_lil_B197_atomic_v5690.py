"""Positive reconstruction and semantic rejection tests before registration or ROM mutation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B197_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B197_references_v5687 import FLAGS,OUTPUT as DOC,CHOICE_OUTPUT as MENU,MAP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_atomic_v5690')
PARENT=Path('out/all_routes_combined_v5637_candidate.nds')
SEAL=Path('work/analysis/lil_B197_reference_approval_v5687/approval_receipt.json')
NATIVE=Path('work/analysis/lil_B197_native_approval_v5670/all24_source_prose_current_native_speech_choice_approval.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    verified=read('work/analysis/editorial_handoff_verification_v5675/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert sha(PARENT.read_bytes())==verified['candidate_sha256']
    doc,menu,mapping=map(read,[DOC,MENU,MAP]);terms=read(doc['actor_terminology_reconciliation'])
    parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    deps={str(DOC),str(MENU),str(MAP),str(SEAL),str(NATIVE),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B197_layout_v1.py','dk4tool/dialogue/lil_B197_profile.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py',
        'work/analysis/editorial_handoff_verification_v5675/verified_handoff.json','docs/editorial_testing_scope_v1870.md'}
    deps.update(v for k,v in doc.items() if k.endswith('_sha256') and isinstance(doc.get(k[:-7]),str) and Path(doc[k[:-7]]).is_file() for v in [doc[k[:-7]]])
    deps.update(mapping[k] for k in ['source_plan','source_census']);deps.update(mapping['evidence'])
    excluded={Path(p).resolve() for p in ['translations/release_stack.json','scripts/build_integrated_release.py','translations/editorial_review_current_v1.json','translations/rom_retention_pins.json',*[str(Path('docs')/n) for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
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
    conf=dict(format='dk4-lil-B197-editorial-release-v1',manuscript=str(DOC),choices=str(MENU),reference_map=str(MAP),reference_approval=str(SEAL),native_approval=str(NATIVE),
        required_map_flags=FLAGS,required_term_flags=[k for k,v in terms.items() if v is True],
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,config)
    assert test.read_file(owned.PATH)==Path(read(mapping['source_plan'])['target_SC2']).read_bytes() and len(proof['changed_records'])==24
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
    mutations=[]
    for key in ['source_SC2_sha256','canonical_SC2_sha256','clean_SC2_sha256','clean_ROM_sha256','required_runtime_arm9_sha256','required_runtime_common_sha256','target_SC2_sha256']:
        mutations.append(('wrong-'+key,str(config),lambda v,k=key:v.update({k:'0'*64})))
    mutations += [
        ('missing-speech',str(DOC),lambda v:v['records'].pop()),('missing-label',str(MENU),lambda v:v['records'].pop()),
        ('wrong-policy',str(DOC),lambda v:v.update(translation_policy='natural-dialogue-v1')),('wrong-locale',str(DOC),lambda v:v.update(target_locale='en-GB')),
        ('unchecked-format',str(DOC),lambda v:v.update(formatting_review_pending=True)),
        ('lost-retention-reason',str(DOC),lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
        ('invented-prose',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:AD}Hello, sister.')),
        ('wrong-selector',str(DOC),lambda v:v['records'][0].update(source_selector=2)),
        ('wrong-full-preamble',str(DOC),lambda v:v['records'][0].update(source_complete_preamble_hex='0040ffff0002')),
        ('wrong-source-index',str(DOC),lambda v:v['records'][0].update(source_record_index=4)),
        ('wrong-current-index',str(DOC),lambda v:v['records'][0].update(current_record_index=4)),
        ('wrong-source-reference',str(DOC),lambda v:v['records'][0]['source_reference'].update(offset=14)),
        ('wrong-current-reference',str(DOC),lambda v:v['records'][0]['current_reference'].update(offset=14)),
        ('invented-FI-in-literal-Ian-notice',str(DOC),lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english='{SPEAKER:FE}{MACRO:FI}: Charm +1!')),
        ('R74-ordinary-wrap-waiver-lost',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==74)['qa_waivers'].pop()),
        ('actual-speech-claimed-offline',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==74).update(actual_B22_display_fixture_observed=False)),
        ('invented-haggle-label',str(MENU),lambda v:v['records'][0].update(english='Haggle')),
        ('menu-option-reordered',str(MENU),lambda v:v['records'][0].update(option_index=1)),
        ('menu-owner-changed',str(MENU),lambda v:v['records'][0].update(command_offset=264)),
        ('typed-whole-object-changed',str(MENU),lambda v:v['records'][0].update(typed_target_object_hex='00220000')),
        ('missing-command-map-entry',str(MAP),lambda v:v['blocks'][0]['command_map'].pop()),
        ('missing-independent-map-entry',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
        ('wrong-nested-ancestor',str(MAP),lambda v:next(c for c in v['blocks'][0]['mapped_native_commands'] if c['source_0100_ancestors'])['target_0100_ancestors'].append(8)),
        ('missing-relative-site',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'].pop()),
        ('wrong-relative-target',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=146)),
        ('wrong-relative-unmatched',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_unmatched_next=142)),
        ('wrong-relative-source-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(source_span=6)),
        ('wrong-relative-target-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(target_span=6)),
        ('missing-target-skip-proof',str(MAP),lambda v:v['blocks'][0]['target_native_skip_cases'].pop()),
        ('wrong-source-logical-extent',str(MAP),lambda v:v['blocks'][0].update(source_logical_end=880)),
        ('wrong-target-logical-extent',str(MAP),lambda v:v['blocks'][0].update(research_logical_end=1000)),
        ('wrong-label-offset',str(MAP),lambda v:v['blocks'][0]['choice_commands'][0]['label_references'][0].update(new_offset=v['blocks'][0]['choice_commands'][0]['label_references'][0]['new_offset']+1)),
        ('wrong-label-record-index',str(MAP),lambda v:v['blocks'][0]['choice_commands'][0]['label_references'][0].update(new_record_index=34)),
        ('wrong-speech-record-index',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(new_record_index=6)),
        ('wrong-source-ending',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(source_offset=876)),
        ('wrong-target-ending',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=1000)),
        ('missing-native-plane',doc['native_font_proof'],lambda v:v['cases'].pop()),
        ('clipped-native-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost-native-page',doc['native_font_proof'],lambda v:v['cases'][0].update(one_native_page_consumes_complete_target=False)),
        ('missing-native-negative',doc['native_font_proof'],lambda v:v['negative_controls'].pop()),
        ('missing-formatter-negative',str(NATIVE),lambda v:v['formatter_negatives'].pop()),
        ('missing-stored-case',doc['final_padding_proof'],lambda v:v['final_target_parity_cases'].pop()),
        ('wrong-stored-alignments',doc['final_padding_proof'],lambda v:v.update(current_final_stored_macro_alignment_cases=80)),
        ('wrong-menu-count-calls',doc['final_choice_proof'],lambda v:v.update(fresh_count_calls=1)),
        ('missing-relocated-picture-pair',doc['relocated_control_proof'],lambda v:v['picture_and47xx_current_relocated_pairs'].pop()),
        ('wrong-actor-dispatch',doc['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][0].update(resolved_actor_ID=2)),
        ('missing-opaque-leaf',doc['relocated_control_proof'],lambda v:v['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves'].pop()),
        ('missing-declared-end-probe',doc['termination_decode_proof'],lambda v:v['cases'].pop()),
        ('lost-actual-delegation-index',doc['representative_proof'],lambda v:v.update(actual_original_menu_indices=[0,1])),
        ('missing-actual-panel',load_path:=read(doc['postscene_native_state_proof'])['actual_proof'],lambda v:v['actual_panels'].pop()),
        ('lost-viewed-status',doc['postscene_native_state_proof'],lambda v:v.update(visual_review_pending=True)),
        ('missing-viewed-screen',doc['postscene_native_state_proof'],lambda v:v['all_actual_consumer_menu_sheets_viewed'].pop()),
        ('wrong-R74-exact-wrap-rows',doc['source_bound_wrap_retention_proof'],lambda v:v['visible_rows'].pop()),
        ('weak-wrap-waiver-transferred-to-R5',str(DOC),lambda v:v['records'][0].update(qa_waivers=['weak-line-ending'],qa_waiver_reason='copy')),
        ('wrong-money-term',doc['actor_terminology_reconciliation'],lambda v:v.update(money_term='credits')),
        ('wrong-Ian-notice-name',str(DOC),lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english='{SPEAKER:FE}Rafael: Charm +1!')),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:v['fresh2_actor_names']['rows'][0].update(original_voice_class=0)),
        ('wrong-payment-contract',doc['source_financial_context'],lambda v:v.update(source8500_price_matches_exact_native_payment_amount=False))]
    mutations += [
        ('lost-postscene-difference-honesty',doc['postscene_native_state_proof'],lambda v:v.update(broad_postscene_equivalence_unproven_and_not_substituted_for_source_control_display_and_return_checks=False)),
        ('lost-source-portrait-baseline',doc['postscene_native_state_proof'],lambda v:v.update(source_matched_blank_portrait_name_additional_records=[])),
        ('lost-focused-visible-Pass-proof',doc['postscene_native_state_proof'],lambda v:v.update(initial_menu_sampling_failure_resolved_by16_new_complete_active_highlight_holds_without_retiming=False)),
        ('lost-timing-difference',load_path,lambda v:v['command_timing_differences'].pop()),
        ('lost-world-RGB-difference',load_path,lambda v:v['later_whole_RGB_differences'].pop()),
        ('lost-47xx-mapped-stream-pointer-proof',doc['relocated_control_proof'],lambda v:v.update(original47xx_R3_is_exact_mapped_stream_instruction_pointer=False))]
    for flag in FLAGS:mutations.append(('lost-map-'+flag,str(MAP),lambda v,k=flag:v.update({k:False})))
    for flag in conf['required_term_flags']:mutations.append(('lost-source-context-'+flag,doc['actor_terminology_reconciliation'],lambda v,k=flag:v.update({k:False})))
    for label,path,edit in mutations:reject(label,path,edit)
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,semantic_load_overrides_leave_real_hashes_intact_to_exercise_guards=True,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'atomic_validation_receipt.json',dict(positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),
        negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,config=str(config),config_sha256=sha(config.read_bytes()),
        parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=24,dependencies=len(conf['dependencies']),new_ROMs=0,new_review_credit=0,full_goal_complete=False))
    print(dict(positive_records=24,semantic_negatives=len(negatives),dependencies=len(conf['dependencies']),all_before_mutation=True))
