"""Validate atomic B194 integration and append its profile after complete V5478."""
import ast
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B194_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B194_registration_v5530')
PROFILE='all-routes-unified-v5531'
PARENT=Path('out/all_routes_combined_v5478_candidate.nds')
DOC=Path('translations/lil_B194_editorial_manuscript_v4.json')
MAP=Path('translations/lil_B194_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    verified=read('work/analysis/editorial_handoff_verification_v5528/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert sha(PARENT.read_bytes())==verified['candidate_sha256'] and PROFILE not in registry['profiles']
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    doc,mapping=read(DOC),read(MAP);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MAP),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B194_layout_v1.py','dk4tool/dialogue/lil_B194_profile.py','dk4tool/dialogue/layout.py',
        'dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md',
        'work/analysis/lil_B194_reference_approval_v5526/approval_receipt.json',
        'work/analysis/lil_B194_loader_v5510/whole_SC2_and_B194_initial_entry_proof.json',
        'work/analysis/editorial_handoff_verification_v5528/verified_handoff.json'}
    keys=['source_context','native_font_proof','source_nameplate_consumer_proof','final_padding_proof','relocated_control_proof',
        'representative_proof','termination_decode_proof','actor_voice_contract','effective_current_comparison','whole_exchange_context_notes',
        'branch_proof','source_entry_proof','control_contract','actor_terminology_reconciliation','source_effect_and_predicate_contract',
        'postscene_native_state_proof','current_C200_source_ownership_proof','layout_QA_proof']
    deps.update(doc[k] for k in keys);deps.update(mapping[k] for k in ['source_plan','source_census'])
    native_approval='work/analysis/lil_B194_native_approval_v5503/all11_source_prose_current_native_approval.json'
    actual_proof=doc['postscene_native_state_proof']
    deps.update([native_approval,actual_proof])
    excluded={p.resolve() for p in [rp,builder,Path('translations/editorial_review_current_v1.json'),Path('translations/rom_retention_pins.json'),
        *[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]]}
    pending=list(deps);seen=set()
    while pending:
        p=pending.pop()
        if p in seen:continue
        seen.add(p)
        if Path(p).suffix!='.json':continue
        value=read(p)
        if not isinstance(value,dict):continue
        for key in ['evidence','dependencies']:
            if not isinstance(value.get(key),dict):continue
            for item in value[key]:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:deps.add(item);pending.append(item)
    native,sample,visual=[read(doc[k]) for k in ['native_font_proof','representative_proof','postscene_native_state_proof']]
    deps.update(s['path'] for s in native['review_sheets']+sample['viewed_actual_sheets'])
    deps.update(r['preview'] for r in native['cases']);deps.update(s['path'] for v in visual['versions'] for s in v['viewed_sheets'])
    conf=dict(format='dk4-lil-B194-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],
        clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        native_approval=native_approval,actual_proof=actual_proof,dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,positive)
    expected=Path(read(mapping['source_plan'])['target_SC2']).read_bytes()
    assert test.read_file(owned.PATH)==expected and len(proof['changed_records'])==11
    save(ROOT/'positive_reconstruction.json',proof)
    negatives=[];original_load=owned.load
    def reject(label,path,edit):
        image=NdsImage.open(PARENT);paths=[owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4'];initial=[image.read_file(p) for p in paths]
        value=deepcopy(read(path));before_value=deepcopy(value);edit(value);assert value!=before_value,label
        def changed_load(p):return deepcopy(value) if str(Path(p))==str(Path(path)) else original_load(p)
        owned.load=changed_load
        try:
            try:owned.apply_release(image,baseline,positive)
            except (ValueError,AssertionError,KeyError) as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
            else:raise AssertionError('Accepted negative:'+label)
        finally:owned.load=original_load
        assert initial==[image.read_file(p) for p in paths],label
    for key in ['format','required_runtime_arm9_sha256','required_runtime_common_sha256','source_SC2_sha256','canonical_SC2_sha256','clean_ROM_sha256','clean_SC2_sha256','target_SC2_sha256']:
        reject('config-'+key,positive,lambda v,k=key:v.update({k:'0'*64}))
    reject('changed-dependency',positive,lambda v:v['dependencies'].update({str(DOC):'0'*64}))
    mutations=[
        ('missing-source-gate',str(DOC),lambda v:v['records'][0]['review'].update(source=False)),
        ('missing-speech',str(DOC),lambda v:v['records'].pop()),
        ('wrong-source-offset',str(DOC),lambda v:v['records'][0]['source_reference'].update(offset=1)),
        ('wrong-current-offset',str(DOC),lambda v:v['records'][0]['current_reference'].update(offset=1)),
        ('wrong-source-header',str(DOC),lambda v:v['records'][0]['source_reference'].update(header_offset=1)),
        ('wrong-current-header',str(DOC),lambda v:v['records'][0]['current_reference'].update(header_offset=1)),
        ('wrong-source-length',str(DOC),lambda v:v['records'][0]['source_reference'].update(bytes=1)),
        ('wrong-current-length',str(DOC),lambda v:v['records'][0]['current_reference'].update(bytes=1)),
        ('wrong-source-record-index',str(DOC),lambda v:v['records'][0]['source_reference'].update(record_index=1)),
        ('wrong-current-record-index',str(DOC),lambda v:v['records'][0].update(current_record_index=1)),
        ('wrong-source-block',str(DOC),lambda v:v['records'][0]['source_reference'].update(block=193)),
        ('changed-English',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:9C}Hello.')),
        ('manual-break',str(DOC),lambda v:v['records'][0].update(english=v['records'][0]['english']+'{LB}')),
        ('manual-padding',str(DOC),lambda v:v['records'][0].update(english=v['records'][0]['english']+'{PAD}')),
        ('FE-progressive',str(DOC),lambda v:next(r for r in v['records'] if r['source_selector']==254).update(kind='progressive')),
        ('lost-retention-reason',str(DOC),lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
        ('lost-actual-scope',str(DOC),lambda v:v['records'][0].update(actual_B22_display_fixture_observed=False)),
        ('lost-FI',str(DOC),lambda v:next(r for r in v['records'] if '{MACRO:FI}' in r['english']).update(english='{SPEAKER:06}Admiral, did you hear that?')),
        ('FI-replaced-by-literal-Lil',str(DOC),lambda v:next(r for r in v['records'] if '{MACRO:FI}' in r['english']).update(english='{SPEAKER:06}Admiral Lil, did you hear that?')),
        ('FI-changed-to-FO',str(DOC),lambda v:next(r for r in v['records'] if '{MACRO:FI}' in r['english']).update(english='{SPEAKER:06}Admiral {MACRO:FO}, did you hear that?')),
        ('missing-end-map',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong-end-map',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=540)),
        ('invented-pause',str(MAP),lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].append({})),
        ('invented-choice',str(MAP),lambda v:v['blocks'][0]['choice_commands'].append({})),
        ('wrong-stored-offset',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(new_offset=1)),
        ('wrong-parity',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(parity_space_added=not v['blocks'][0]['text_records'][0]['parity_space_added'])),
        ('wrong-target-hash',str(MAP),lambda v:v['blocks'][0].update(target_block_sha256='0'*64)),
        ('missing-command',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
        ('inconsistent-command-map',str(MAP),lambda v:v['blocks'][0]['command_map'][0].update(new_extent=2)),
        ('wrong-source-extent',str(MAP),lambda v:v['blocks'][0].update(source_bytes=1)),
        ('wrong-source-logical-end',str(MAP),lambda v:v['blocks'][0].update(source_logical_end=1)),
        ('wrong-target-extent',str(MAP),lambda v:v['blocks'][0].update(research_bytes=1)),
        ('wrong-target-logical-end',str(MAP),lambda v:v['blocks'][0].update(research_logical_end=1)),
        ('missing-relative',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'].pop()),
        ('changed-relative-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][2].update(target_span=0)),
        ('changed-zero-relative-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][3].update(source_span=4)),
        ('wrong-relative-operand-field',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(span_field_offset=1)),
        ('missing-skip-case',str(MAP),lambda v:v['blocks'][0]['target_native_skip_cases'].pop()),
        ('wrong-skip-extent',str(MAP),lambda v:v['blocks'][0]['target_native_skip_cases'][0].update(native_extent=100)),
        ('wrong-relative-ancestry',str(MAP),lambda v:next(c for c in v['blocks'][0]['mapped_native_commands'] if c['target_0100_ancestors']).update(target_0100_ancestors=[])),
        ('missing-predicate-scratch-proof',doc['relocated_control_proof'],lambda v:v.update(changed_unaligned_operand_scratch_owned_and_restored=False)),
        ('forced-predicate-result',doc['relocated_control_proof'],lambda v:v['unforced_relocated_predicate_cases'][0]['case'].update(native_result=[2,1,0,0,0,0])),
        ('missing-owned-predicate-write',doc['relocated_control_proof'],lambda v:v['unforced_relocated_predicate_cases'][0]['case']['original_unaligned_operand_read_scratch_writes'].pop()),
        ('wrong-C200-descriptor',doc['relocated_control_proof'],lambda v:v['relocated_C200_prior_result_cases'][0]['case'].update(source_owned_UI_request_words=[1,0,13,0,0,0,1])),
        ('missing-second-C200-prior',doc['relocated_control_proof'],lambda v:v['relocated_C200_prior_result_cases'].pop()),
        ('lost-resource-prior',doc['relocated_control_proof'],lambda v:v['relocated_resource42_prior_result_cases'].pop()),
        ('wrong-resource-result',doc['relocated_control_proof'],lambda v:v['relocated_resource42_prior_result_cases'][0]['case'].update(native_result=[3,9,0,0,0,0])),
        ('lost-end-prior',doc['relocated_control_proof'],lambda v:v['relocated_end_prior_result_cases'].pop()),
        ('lost-first-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('wrong-bounds',doc['native_font_proof'],lambda v:v['cases'][0].update(all_visible_origins_zero_and_within_four_rows=False)),
        ('lost-page',doc['native_font_proof'],lambda v:v['cases'][0].update(one_native_page_consumes_complete_target=False)),
        ('missing-alignment',doc['native_font_proof'],lambda v:v['cases'][0]['current_native_macro_pipelines'][0]['cases'].pop()),
        ('false-consumer-negative',doc['native_font_proof'],lambda v:v['negative_controls'][0].update(rejected=False)),
        ('lost-FE-plane',doc['native_font_proof'],lambda v:v.update(complete_FE_logical_and_physical_planes=0)),
        ('wrong-name',doc['source_nameplate_consumer_proof'],lambda v:v['native_six_consumer_cases']['rows'][0].update(text='Grandpa')),
        ('wrong-progressive-role',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'156':'Retainer'})),
        ('wrong-full-catalogue-role',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'156':'Sailor'})),
        ('lost-Julio-owned-scratch',doc['source_nameplate_consumer_proof'],lambda v:v['native_six_consumer_cases']['rows'][0].update(original_scratch_rings=[])),
        ('wrong-original-voice',doc['actor_voice_contract'],lambda v:next(r for r in v['fresh3_actor_names']['rows'] if r['actor_ID']==6).update(original_voice_class=0)),
        ('missing-stored-case',doc['final_padding_proof'],lambda v:v['final_target_parity_cases'].pop()),
        ('false-guarded-end',doc['termination_decode_proof'],lambda v:v.update(all2_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('wrong-commodity',doc['actor_terminology_reconciliation'],lambda v:v.update(commodity='Rice')),
        ('wrong-city',doc['actor_terminology_reconciliation'],lambda v:v['one_source_current_city_alias'].update(text='Amsterdam')),
        ('wrong-FI-length',doc['actor_terminology_reconciliation'],lambda v:v.update(FI_default_ASCII_bytes=4)),
        ('invented-title',doc['actor_terminology_reconciliation'],lambda v:v.update(source_supported_English_title='King')),
        ('unresolved-layout',doc['layout_QA_proof'],lambda v:v['failures'].append({'unresolved':True})),
        ('unviewed-native-sheet',native_approval,lambda v:v['reviewed_sheets'][0].update(viewed_in_full_current_turn=False)),
        ('lost-actual-unique-object',actual_proof,lambda v:v.update(unique_actual_display_objects=10)),
        ('missing-actual-setup',actual_proof,lambda v:v['versions'].pop()),
        ('wrong-actual-return',actual_proof,lambda v:v['versions'][0].update(return_frames=[9001,9001])),
        ('wrong-actual-predicate',actual_proof,lambda v:v['versions'][1].update(predicate_result=0)),
        ('invented-PRNG-inequality',actual_proof,lambda v:v['versions'][0].update(final_PRNG_seeds=[1,2])),
        ('wrong-timing-disclosure',actual_proof,lambda v:v['versions'][0]['timing_differences'].update(total=1)),
        ('concealed-state-difference',actual_proof,lambda v:v['versions'][0].update(all_five_native_groups_and_whole1A04_actor_and_captain2_equal=False)),
        ('unviewed-full-screen',actual_proof,lambda v:v['versions'][1]['viewed_sheets'][-1].update(viewed_after_image_return=False)),
        ('concealed-setup',doc['representative_proof'],lambda v:v.update(extra_original_B165_recruitment_initializer_is_disclosed_test_setup_not_earned_progress=False)),
        ('lost-conditional-UI-resource-actual-scope',doc['representative_proof'],lambda v:v.update(source_resource42_and_two_C200_paths_observed_in_conditional_setup=False)),
    ]
    for flag in ['rice_ingredient_remains_reported_not_recipe_technical_process_origin_or_narrator_fact',
        'legendary_liquor_is_Julios_excited_inference_not_certified_identity_award_or_earned_item',
        'source_now_drink_invitation_and_later_urgent_purchase_are_intentions_not_completed_actions',
        'no_invented_brotherhood_player_employment_shared_drinking_history_or_new_personal_name',
        'no_price_amount_measured_serving_venue_recipe_origin_health_effect_intoxication_or_reward_invented',
        'Sake37_older_UI_fidelity_review_remains_open_separate_from_dialogue',
        'tentative_Sake_Hangzhou_FE_not_earlier_location_or_earned_fashion']:
        mutations.append(('lost-source-context-'+flag,doc['actor_terminology_reconciliation'],lambda v,k=flag:v.update({k:False})))
    for label,path,edit in mutations:reject(label,path,edit)
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,producer_sha256=sha(Path(__file__).read_bytes())))
    stage=b'''    lil_proof = profile_config.get('lil_B194_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B194_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B194_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B194 must run once after the complete V5478 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B194_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before)
    save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v5478'])
    profile.update(status='experimental',lil_B194_editorial=owned.CONFIG,
        description='Complete V5478 plus11 B194 contextual sake-exchange reviews:4 revisions/7 justified retentions. Preserve rice hearsay,causal immediate invitation,Julio stammer/fabled-drink belief,source Admiral FI address,personal urgent purchase intention and prospective Sake/Hangzhou notice. All21 commands,four relative spans,one predicate,resource42,two C200 and end remain. Source540/540 becomes516/514 with exact inverse. Both unforced paths pass in four disclosed content cold boots,including one original recruitment setup;79 holds,230 nontext pairs and24 full screens pass. Registered cumulative build and current startup pending.',
        note='Source/native/reference/representative approved;registered build,exact patch and current startup pending.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v5530.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    data=(json.dumps(registry,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    with rp.open('r+b') as stream:stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    check=deepcopy(read(rp));check['profiles'].pop(PROFILE)
    assert check==read(ROOT/'release_stack.before.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v5478',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={str(DOC):sha(DOC.read_bytes())},
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),
        negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,
        expected_manifest_batches=578,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(registered=PROFILE,positive_records=11,negative_cases=len(negatives),expected_batches=578,accepted=114,promotion_unchanged=True))
