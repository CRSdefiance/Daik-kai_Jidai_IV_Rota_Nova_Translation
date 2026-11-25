"""Validate atomic B191 integration and append its profile after complete V5346."""
import ast
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B191_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B191_registration_v5395')
PROFILE='all-routes-unified-v5396'
PARENT=Path('out/all_routes_combined_v5346_candidate.nds')
DOC=Path('translations/lil_B191_editorial_manuscript_v5.json')
MAP=Path('translations/lil_B191_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    verified=read('work/analysis/editorial_handoff_verification_v5352/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert sha(PARENT.read_bytes())==verified['candidate_sha256'] and PROFILE not in registry['profiles']
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    doc,mapping=read(DOC),read(MAP);parent=NdsImage.open(PARENT);baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MAP),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B191_layout_v3.py','dk4tool/dialogue/lil_B191_profile.py','dk4tool/dialogue/layout.py',
        'dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md',
        'work/analysis/lil_B191_reference_approval_v5393/approval_receipt.json',
        'work/analysis/lil_B191_loader_v5382/whole_SC2_and_B191_initial_entry_proof.json',
        'work/analysis/editorial_handoff_verification_v5352/verified_handoff.json'}
    keys=['source_context','native_font_proof','source_nameplate_consumer_proof','final_padding_proof','relocated_control_proof',
        'representative_proof','termination_decode_proof','actor_voice_contract','effective_current_comparison','whole_exchange_context_notes',
        'branch_proof','source_entry_proof','control_contract','actor_terminology_reconciliation','source_effect_and_predicate_contract',
        'postscene_native_state_proof','current_C200_source_ownership_proof','layout_retention_review_proof','carried_result_proof','source_bound_wrap_refinement_proof']
    deps.update(doc[k] for k in keys);deps.update(mapping[k] for k in ['source_plan','source_census'])
    native_approval='work/analysis/lil_B191_native_approval_v5376/all13_source_prose_current_native_approval.json'
    actual_proof='work/analysis/lil_B191_actual_v5389/actual_all13_progressive_FE_RNG_effect_or_no_effect_C200_and_single_end.json'
    operand='work/analysis/lil_B191_predicates_v5379/all36_original_mixed_predicate_ownership_cases.json'
    deps.update([native_approval,actual_proof,operand])
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
    deps.update(r['preview'] for r in native['cases']);deps.update(r['path'] for r in visual['paired_full_screen_views'])
    conf=dict(format='dk4-lil-B191-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],
        clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        native_approval=native_approval,actual_proof=actual_proof,operand_ownership_proof=operand,dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,positive)
    expected=Path(read(mapping['source_plan'])['target_SC2']).read_bytes()
    assert test.read_file(owned.PATH)==expected and len(proof['changed_records'])==13
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
        ('changed-English',str(DOC),lambda v:v['records'][0].update(english='{SPEAKER:56}Hello.')),
        ('manual-break',str(DOC),lambda v:v['records'][0].update(english=v['records'][0]['english']+'{LB}')),
        ('manual-padding',str(DOC),lambda v:v['records'][0].update(english=v['records'][0]['english']+'{PAD}')),
        ('FE-progressive',str(DOC),lambda v:next(r for r in v['records'] if r['source_selector']==254).update(kind='progressive')),
        ('lost-retention-reason',str(DOC),lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
        ('lost-actual-scope',str(DOC),lambda v:v['records'][0].update(actual_B22_display_fixture_observed=False)),
        ('missing-end-map',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong-end-map',str(MAP),lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=540)),
        ('missing-relative',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'].pop()),
        ('wrong-relative-span',str(MAP),lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(target_span=2)),
        ('missing-native-skip-case',str(MAP),lambda v:v['blocks'][0]['target_native_skip_cases'].pop()),
        ('invented-pause',str(MAP),lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].append({})),
        ('invented-choice',str(MAP),lambda v:v['blocks'][0]['choice_commands'].append({})),
        ('wrong-stored-offset',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(new_offset=1)),
        ('wrong-parity',str(MAP),lambda v:v['blocks'][0]['text_records'][0].update(parity_space_added=not v['blocks'][0]['text_records'][0]['parity_space_added'])),
        ('wrong-target-hash',str(MAP),lambda v:v['blocks'][0].update(target_block_sha256='0'*64)),
        ('missing-command',str(MAP),lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
        ('missing-predicate',doc['relocated_control_proof'],lambda v:v['predicate_pairs'].pop()),
        ('wrong-RNG-transition',doc['relocated_control_proof'],lambda v:v['predicate_pairs'][0]['cases'][0].update(after_seed=0)),
        ('forced-RNG-fixture',doc['relocated_control_proof'],lambda v:v['predicate_pairs'][0]['cases'][0].update(unforced_current_snapshot=False)),
        ('wrong-C200-descriptor',doc['relocated_control_proof'],lambda v:v['C200_pairs'][0]['cases'][0].update(source_owned_UI_request_words=[1,0,13,0,0,0,1])),
        ('missing-alternative',doc['relocated_control_proof'],lambda v:v['A000_structural_pairs'].pop()),
        ('missing-structural-path',doc['relocated_control_proof'],lambda v:v['all125_source_and_relocated_structural_paths_identical'].pop()),
        ('lost-first-glyph',doc['native_font_proof'],lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('wrong-bounds',doc['native_font_proof'],lambda v:v['cases'][0].update(all_visible_origins_zero_and_within_four_rows=False)),
        ('lost-page',doc['native_font_proof'],lambda v:v['cases'][0].update(one_native_page_consumes_complete_target=False)),
        ('missing-alignment',doc['native_font_proof'],lambda v:v['cases'][0]['current_native_macro_pipelines'][0]['cases'].pop()),
        ('false-negative',doc['native_font_proof'],lambda v:v['negative_controls'][0].update(rejected=False)),
        ('wrong-name',doc['source_nameplate_consumer_proof'],lambda v:v['native_four_consumer_cases']['rows'][0].update(text='Duchess')),
        ('missing-stored-case',doc['final_padding_proof'],lambda v:v['final_target_parity_cases'].pop()),
        ('false-guarded-end',doc['termination_decode_proof'],lambda v:v.update(all2_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('false-actual-panel',actual_proof,lambda v:v.update(complete_matching_observations=12)),
        ('missing-actual-version',actual_proof,lambda v:v['versions'].pop()),
        ('wrong-actual-end',actual_proof,lambda v:v['versions'][0]['selected_B22_command_pairs'][-1].update(original_source_offset=570)),
        ('wrong-actual-effect',actual_proof,lambda v:v['observed_random_path_difference']['original_effects_by_case'].update(reviewed_English=[584])),
        ('concealed-final-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=True)),
        ('invented-town-difference',doc['postscene_native_state_proof'],lambda v:v['postscene9001_native_component_equality'].update(persistent_objects=False)),
        ('lost-indicator-difference',doc['postscene_native_state_proof'],lambda v:v['sampled_postscene_whole_RGB_differences_unmasked'].pop()),
        ('unviewed-full-screen',doc['postscene_native_state_proof'],lambda v:v['paired_full_screen_views'][0].update(viewed_after_image_return=False)),
    ]
    mutations.extend([
        ('missing-operand-case',operand,lambda v:v['cases'].pop()),
        ('wrong-native-RNG-write-address',operand,lambda v:next(r for r in v['cases'] if r['version']=='current')['all_original_native_writes'][0].update(address=0x02279604)),
        ('wrong-native-RNG-write-value',operand,lambda v:next(r for r in v['cases'] if r['version']=='current')['all_original_native_writes'][0].update(value=501)),
        ('unowned-write-approved',operand,lambda v:v['cases'][0].update(full4MiB_difference_exactly_original_owned_RNG_and_optional_operand_scratch=False)),
        ('emulator-seed-forcing',operand,lambda v:v.update(actual_emulator_seed_writes=1)),
        ('missing-threshold-boundary',operand,lambda v:v['cases'][0].update(roll=(v['cases'][0]['roll']+1)%1000)),
    ])
    mutations.extend([
        ('wrong-source-header-metadata',str(DOC),lambda v:v['records'][0]['source_reference'].update(header_offset=1)),
        ('wrong-current-header-metadata',str(DOC),lambda v:v['records'][0]['current_reference'].update(header_offset=1)),
        ('wrong-source-length-metadata',str(DOC),lambda v:v['records'][0]['source_reference'].update(bytes=1)),
        ('wrong-current-length-metadata',str(DOC),lambda v:v['records'][0]['current_reference'].update(bytes=1)),
        ('wrong-source-record-index',str(DOC),lambda v:v['records'][0]['source_reference'].update(record_index=1)),
        ('wrong-current-record-index',str(DOC),lambda v:v['records'][0].update(current_record_index=1)),
        ('wrong-source-block-metadata',str(DOC),lambda v:v['records'][0]['source_reference'].update(block=183)),
        ('wrong-source-extent-metadata',str(MAP),lambda v:v['blocks'][0].update(source_bytes=1)),
        ('wrong-source-logical-metadata',str(MAP),lambda v:v['blocks'][0].update(source_logical_end=1)),
        ('wrong-target-extent-metadata',str(MAP),lambda v:v['blocks'][0].update(research_bytes=1)),
        ('wrong-target-logical-metadata',str(MAP),lambda v:v['blocks'][0].update(research_logical_end=1)),
        ('inconsistent-command-map',str(MAP),lambda v:v['blocks'][0]['command_map'][0].update(new_extent=2)),
        ('lost-layout-reason',doc['layout_retention_review_proof'],lambda v:v['retained_layouts'][0].update(reason='')),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:next(r for r in v['fresh2_actor_names']['rows'] if r['actor_ID']==154).update(original_voice_class=0)),
        ('wrong-progressive-role',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'154':'Retainer'})),
        ('wrong-catalogue-role',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'154':'Sailor'})),
        ('wrong-city-alias',doc['actor_terminology_reconciliation'],lambda v:v['two_source_current_city_aliases'][0].update(text='Amsterdam')),
        ('invented-kinship',doc['actor_terminology_reconciliation'],lambda v:v.update(familiar_oyajisan_does_not_prove_fatherhood_age_or_employment_relation=False)),
        ('lost-buyout-urgency-and-profit-claims',doc['actor_terminology_reconciliation'],lambda v:v.update(exclusive_color_competitor_buyout_popularity_imminent_sellout_and_conditional_profit_are_source_explicit_character_claims=False)),
        ('lost-repeated-doubt',doc['actor_terminology_reconciliation'],lambda v:v.update(two_identical_soukanaa_doubts_and_distinct_soudesu_soudesutte_replies_preserved=False)),
        ('invented-verified-profit',doc['actor_terminology_reconciliation'],lambda v:v.update(no_narrator_verified_shortage_stock_price_rise_guaranteed_profit_or_earned_game_mechanic=False)),
        ('wrong-category-as-commodity',doc['actor_terminology_reconciliation'],lambda v:v.update(category_index=42)),
        ('wrong-category-consumer',doc['actor_terminology_reconciliation'],lambda v:v['current_category_binding']['rows'][-1].update(text='Med')),
        ('lost-clean-first-disclosure',doc['actor_terminology_reconciliation'],lambda v:v.update(no_predecessor_English_exposed=False)),
        ('missing-carried-result-case',doc['carried_result_proof'],lambda v:v['cases'].pop()),
        ('wrong-native-end-prior-result',doc['carried_result_proof'],lambda v:v['cases'][2].update(end_native_result=[0,0,0,0,0,0])),
        ('lost-carried-result-flag',doc['carried_result_proof'],lambda v:v.update(original_interpreter_preserves_caller_second_result_word=False)),
        ('wrong-actual-end-result',actual_proof,lambda v:v['versions'][0]['selected_B22_command_pairs'][-1].update(result_words=[0,0])),
        ('wrong-second700-threshold',doc['relocated_control_proof'],lambda v:v['predicate_pairs'][1]['cases'][0].update(threshold=500)),
        ('wrong-owned700-threshold',operand,lambda v:next(r for r in v['cases'] if r['offset']==28).update(threshold=500)),
        ('duplicate-owned-site',operand,lambda v:v['cases'][0].update(offset=28)),
        ('invented-actual-effect',actual_proof,lambda v:v['versions'][0]['source_A000'].append({'word':40960})),
        ('wrong-second-actual-draw',actual_proof,lambda v:v['versions'][0]['actual_predicate_transitions'][1].update(source_offset=28)),
        ('lost-R64-wrap-proof',doc['source_bound_wrap_refinement_proof'],lambda v:v.update(all13_words_controls_and_prose_unchanged=False)),
        ('concealed-other-wrap-changes',doc['source_bound_wrap_refinement_proof'],lambda v:v.update(twelve_other_compiled_targets_exact=False)),
        ('lost-R64-boundary-reason',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==64).pop('reviewed_ordinary_boundaries')),
        ('lost-wrap-mutation-control',doc['source_bound_wrap_refinement_proof'],lambda v:v['exact_source_and_prose_mutation_controls'].pop()),
        ('unreviewed-other-boundary',str(DOC),lambda v:v['records'][0].update(reviewed_ordinary_boundaries=[{'after_word':'dye'}])),
            ('wrong-timing-disclosure',doc['postscene_native_state_proof'],lambda v:v['exact_timing_difference_counts'].update(total=0)),
        ('lost-FE',doc['native_font_proof'],lambda v:v.update(complete_FE_logical_and_physical_planes=0)),
        ('wrong-actual-unforced-flag',actual_proof,lambda v:v['versions'][0]['actual_predicate_transitions'][0].update(actual_unforced_original_LCG_transition=False)),
    ])
    for label,path,edit in mutations:reject(label,path,edit)
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,producer_sha256=sha(Path(__file__).read_bytes())))
    stage=b'''    lil_proof = profile_config.get('lil_B191_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B191_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B191_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B191 must run once after the complete V5346 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B191_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before)
    save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v5346'])
    profile.update(status='experimental',lil_B191_editorial=owned.CONFIG,
        description='Complete V5346 plus13 B191 whole-exchange reviews:5 revisions/8 justified retentions. Shopkeeper86/Sailor154 discuss a dye color. Restore buyout warning,urgency,rapid depletion,delegation and kinship-free familiar profit reassurance;retain repeated doubts/answers and the tentative Dyes/Calicut notice. Profit/shortage are speaker claims. Four source names,voices0/4,category14 and two city aliases bind. Exact R64 source/prose soft wrap uses2 safe rows with every word unchanged. All38 commands,three500/700/500 predicates,16branches,four effects and no-effect paths,C200,end and source2 tailzeros restore exactly. Source736/734 becomes680/680. Two9001-frame content boots show13 panels,51holds,115nontext pairs,20fullscreens and normal return. Both unforced875/988 draws select the original no-effect path. Returns5977/5975,twelve timings,four original indicators and unequal final PRNG are disclosed;final RGB,five native groups and whole actor agree. No natural activation,earned state or actual execution of the four alternative effects is claimed.',
        note='Source/native/reference/representative approved;registered build,exact patch and current startup pending.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v5395.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    data=(json.dumps(registry,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    with rp.open('r+b') as stream:stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    check=deepcopy(read(rp));check['profiles'].pop(PROFILE)
    assert check==read(ROOT/'release_stack.before.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v5346',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={str(DOC):sha(DOC.read_bytes())},
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),
        negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,
        expected_manifest_batches=575,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4701',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(registered=PROFILE,positive_records=13,negative_cases=len(negatives),expected_batches=575,accepted=114,promotion_unchanged=True))
