"""Positive reconstruction and semantic rejection tests before registration or ROM mutation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B196_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.seal_lil_B196_references_v5631 import FLAGS,OUTPUT as DOC,CHOICE_OUTPUT as MENU,MAP
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B196_atomic_v5635b')
PARENT=Path('out/all_routes_combined_v5580_candidate.nds')
SEAL=Path('work/analysis/lil_B196_reference_approval_v5631/approval_receipt.json')
NATIVE=Path('work/analysis/lil_B196_native_approval_v5612/all36_source_prose_current_native_speech_choice_approval.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    verified=read('work/analysis/editorial_handoff_verification_v5633/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert sha(PARENT.read_bytes())==verified['candidate_sha256']
    doc,menu,mapping=map(read,[DOC,MENU,MAP]);terms=read(doc['actor_terminology_reconciliation'])
    parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    deps={str(DOC),str(MENU),str(MAP),str(SEAL),str(NATIVE),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B196_layout_v3.py','dk4tool/dialogue/lil_B196_profile_v2.py','dk4tool/dialogue/layout.py','dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py',
        'work/analysis/editorial_handoff_verification_v5633/verified_handoff.json','docs/editorial_testing_scope_v1870.md'}
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
    conf=dict(format='dk4-lil-B196-editorial-release-v1',manuscript=str(DOC),choices=str(MENU),reference_map=str(MAP),reference_approval=str(SEAL),native_approval=str(NATIVE),
        required_map_flags=FLAGS,required_term_flags=[k for k,v in terms.items() if v is True],
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],clean_SC2_sha256=mapping['clean_SC2_sha256'],
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);config=ROOT/'positive_config.json';save(config,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,config)
    assert test.read_file(owned.PATH)==Path(read(mapping['source_plan'])['target_SC2']).read_bytes() and len(proof['changed_records'])==36
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
        ('FI-changed-to-literal-name',str(DOC),lambda v:next(r for r in v['records'] if r['kind']=='system-FE').update(english='{SPEAKER:FE}Lil: Charm +1!')),
        ('R74-ordinary-boundary-approval-lost',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==74)['reviewed_ordinary_boundaries'].pop()),
        ('offline-conditional-claimed-as-gameplay',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==74).update(actual_B22_display_fixture_observed=True)),
        ('invented-haggle-label',str(MENU),lambda v:v['records'][0].update(english='Haggle')),
        ('menu-option-reordered',str(MENU),lambda v:v['records'][0].update(option_index=1)),
        ('menu-owner-changed',str(MENU),lambda v:v['records'][0].update(command_offset=582)),
        ('typed-whole-object-changed',str(MENU),lambda v:v['records'][0].update(typed_target_object_hex='00210000')),
        ('missing-command-map-entry',str(MAP),lambda v:v['blocks'][0]['command_map'].pop()),
        ('missing-independent-map-entry',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
        ('wrong-nested-ancestor',str(MAP),lambda v:next(c for c in v['blocks'][0]['mapped_native_commands'] if c['source_0100_ancestors'])['target_0100_ancestors'].append(8)),
        ('missing-relative-site',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'].pop()),
        ('wrong-relative-target',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=146)),
        ('wrong-relative-unmatched',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_unmatched_next=142)),
        ('wrong-relative-source-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(source_span=6)),
        ('wrong-relative-target-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(target_span=6)),
        ('missing-target-skip-proof',str(MAP),lambda v:v['blocks'][0]['target_native_skip_cases'].pop()),
        ('wrong-source-logical-extent',str(MAP),lambda v:v['blocks'][0].update(source_logical_end=1816)),
        ('wrong-target-logical-extent',str(MAP),lambda v:v['blocks'][0].update(research_logical_end=1666)),
        ('wrong-label-offset',str(MAP),lambda v:v['blocks'][0]['choice_commands'][0]['label_references'][0].update(new_offset=204)),
        ('wrong-label-record-index',str(MAP),lambda v:v['blocks'][0]['choice_commands'][0]['label_references'][0].update(new_record_index=34)),
        ('wrong-speech-record-index',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(new_record_index=6)),
        ('wrong-source-ending',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(source_offset=366)),
        ('wrong-target-ending',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=318)),
        ('missing-native-plane',doc['native_font_proof'],lambda v:v['cases'].pop()),
        ('clipped-native-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost-native-page',doc['native_font_proof'],lambda v:v['cases'][0].update(one_native_page_consumes_complete_target=False)),
        ('missing-native-negative',doc['native_font_proof'],lambda v:v['negative_controls'].pop()),
        ('missing-formatter-negative',str(NATIVE),lambda v:v['formatter_negatives'].pop()),
        ('missing-stored-case',doc['final_padding_proof'],lambda v:v['final_target_parity_cases'].pop()),
        ('wrong-stored-alignments',doc['final_padding_proof'],lambda v:v.update(current_final_stored_macro_alignment_cases=92)),
        ('wrong-menu-count-calls',doc['final_choice_proof'],lambda v:v.update(fresh_count_calls=10)),
        ('missing-relocated-predicate',doc['relocated_control_proof'],lambda v:v['relocated_unforced_predicates'].pop()),
        ('wrong-actor-dispatch',doc['relocated_control_proof'],lambda v:v['relocated_dispatch_cases'][0].update(resolved_actor_ID=2)),
        ('missing-opaque-leaf',doc['relocated_control_proof'],lambda v:v['all37_source_current_target_nonrelative_nonspeech_nonchoice_leaves'].pop()),
        ('missing-declared-end-probe',doc['termination_decode_proof'],lambda v:v['cases'].pop()),
        ('invented-all-six-Buy-gameplay',doc['representative_proof'],lambda v:v.update(actual_buy_menu_offsets=owned.MENUS)),
        ('missing-actual-panel',load_path:=read(doc['postscene_native_state_proof'])['actual_proof'],lambda v:v['actual_panels'].pop()),
        ('lost-viewed-status',doc['postscene_native_state_proof'],lambda v:v.update(visual_review_pending=True)),
        ('missing-viewed-screen',doc['postscene_native_state_proof'],lambda v:v['all_actual_consumer_menu_sheets_viewed'].pop()),
        ('wrong-record-specific-word-count',doc['source_bound_wrap_retention_proof'],lambda v:v.update(paragraph_words=22)),
        ('missing-wrap-nontransfer-case',doc['source_bound_wrap_retention_proof'],lambda v:v['six_source_or_prose_changes_do_not_inherit_review'].pop()),
        ('wrong-money-term',doc['actor_terminology_reconciliation'],lambda v:v.update(money_term='credits')),
        ('wrong-FI-expansion',doc['actor_terminology_reconciliation'],lambda v:v.update(current_source_FI_expansion='Rafael')),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:v['fresh6_actor_names']['rows'][0].update(original_voice_class=0)),
        ('wrong-payment-contract',doc['source_financial_context'],lambda v:v.update(six_source_prices_match_six_exact_native_payment_amounts=False))]
    for flag in FLAGS:mutations.append(('lost-map-'+flag,str(MAP),lambda v,k=flag:v.update({k:False})))
    for flag in conf['required_term_flags']:mutations.append(('lost-source-context-'+flag,doc['actor_terminology_reconciliation'],lambda v,k=flag:v.update({k:False})))
    for label,path,edit in mutations:reject(label,path,edit)
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,semantic_load_overrides_leave_real_hashes_intact_to_exercise_guards=True,producer_sha256=sha(Path(__file__).read_bytes())))
    save(ROOT/'atomic_validation_receipt.json',dict(positive_proof=str(ROOT/'positive_reconstruction.json'),positive_proof_sha256=sha((ROOT/'positive_reconstruction.json').read_bytes()),
        negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,config=str(config),config_sha256=sha(config.read_bytes()),
        parent_ROM_sha256=sha(PARENT.read_bytes()),positive_records=36,dependencies=len(conf['dependencies']),new_ROMs=0,new_review_credit=0,full_goal_complete=False))
    print(dict(positive_records=36,semantic_negatives=len(negatives),dependencies=len(conf['dependencies']),all_before_mutation=True))
