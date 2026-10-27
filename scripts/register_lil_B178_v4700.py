"""Test positive/atomic-negative B178 compilation, then register after the full V4655 stack."""
import ast
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B178_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B178_registration_v4700')
PROFILE='all-routes-unified-v4701'
PARENT=Path('out/all_routes_combined_v4655_candidate.nds')
DOC=Path('translations/lil_B178_editorial_manuscript_v4.json')
MAP=Path('translations/lil_B178_editorial_relocation_map_v1.json')

if __name__=='__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp,builder=Path('translations/release_stack.json'),Path('scripts/build_integrated_release.py')
    raw,before=rp.read_bytes(),builder.read_bytes();registry=read(rp)
    prior=read('work/analysis/lil_B178_reference_checkpoint_v4697/checkpoint_receipt.json')['preserved_release_files']
    verified=read('work/analysis/editorial_handoff_verification_v4698/verified_handoff.json')
    assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==verified['ledger_sha256']
    assert sha(raw)==prior[rp.as_posix()] and sha(before)==prior[builder.as_posix()]
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4595'
    doc,mapping=read(DOC),read(MAP)
    parent,baseline=NdsImage.open(PARENT),NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']
    deps={str(DOC),str(MAP),str(Path(owned.__file__).relative_to(Path.cwd())),str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B178_layout_v1.py','dk4tool/dialogue/lil_B178_profile.py','dk4tool/dialogue/layout.py',
        'dk4tool/dialogue/encoder.py','dk4tool/dialogue/qa.py','dk4tool/dialogue/review.py','docs/editorial_testing_scope_v1870.md',
        'work/analysis/lil_B178_reference_approval_v4696/approval_receipt.json',
        'work/analysis/lil_B178_loader_v4687/whole_SC2_and_B178_initial_entry_proof.json',
        'work/analysis/editorial_handoff_verification_v4698/verified_handoff.json'}
    deps.update(doc[k] for k in ['source_context','native_font_proof','native_progressive_and_FE_proof','source_nameplate_consumer_proof',
        'final_padding_proof','relocated_control_proof','representative_proof','termination_decode_proof','actor_voice_contract',
        'effective_current_comparison','whole_exchange_context_notes','branch_proof','source_entry_proof','control_contract',
        'actor_terminology_reconciliation','source_effect_and_predicate_contract','postscene_native_state_proof'])
    deps.update(mapping[k] for k in ['source_plan','source_census'])
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
    conf=dict(format='dk4-lil-B178-editorial-release-v1',manuscript=str(DOC),reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')),required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'],target_SC2_sha256=mapping['target_SC2_sha256'],canonical_SC2_sha256=mapping['canonical_SC2_sha256'],
        clean_SC2_sha256=mapping['clean_SC2_sha256'],clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        dependencies={p:sha(Path(p).read_bytes()) for p in sorted(deps)})
    ROOT.mkdir(parents=True);positive=ROOT/'positive_config.json';save(positive,conf)
    test=NdsImage.open(PARENT);proof=owned.apply_release(test,baseline,positive)
    expected=Path(read(mapping['source_plan'])['target_SC2']).read_bytes()
    assert test.read_file(owned.PATH)==expected and len(proof['changed_records'])==13
    save(ROOT/'positive_reconstruction.json',proof)
    negatives=[];original_load=owned.load
    def reject(label,config,overrides=None):
        image=NdsImage.open(PARENT);paths=[owned.PATH,'/__arm9__.bin','/COMMON/MESFILE.DK4'];initial=[image.read_file(p) for p in paths]
        overrides={} if overrides is None else overrides
        def changed_load(p):return deepcopy(overrides[str(Path(p))]) if str(Path(p)) in overrides else original_load(p)
        owned.load=changed_load
        try:
            try:owned.apply_release(image,baseline,config)
            except (ValueError,AssertionError,KeyError) as error:negatives.append(dict(case=label,rejected=True,error=str(error)))
            else:raise AssertionError('Accepted negative:'+label)
        finally:owned.load=original_load
        assert initial==[image.read_file(p) for p in paths],label
    for label,key,value in [('format','format','bad'),('runtime','required_runtime_arm9_sha256','0'*64),('COMMON','required_runtime_common_sha256','0'*64),
        ('source','source_SC2_sha256','0'*64),('canonical','canonical_SC2_sha256','0'*64),('clean_ROM','clean_ROM_sha256','0'*64),
        ('clean_script','clean_SC2_sha256','0'*64),('target','target_SC2_sha256','0'*64)]:
        altered=deepcopy(conf);altered[key]=value;reject('config-'+label,positive,{str(positive):altered})
    altered=deepcopy(conf);altered['dependencies'][str(DOC)]='0'*64;reject('config-dependency',positive,{str(positive):altered})
    mutations=[
        ('missing-source-gate','manuscript',lambda v:v['records'][0]['review'].update(source=False)),
        ('missing-speech','manuscript',lambda v:v['records'].pop()),
        ('wrong-source-offset','manuscript',lambda v:v['records'][0]['source_reference'].update(offset=1)),
        ('wrong-current-offset','manuscript',lambda v:v['records'][0]['current_reference'].update(offset=1)),
        ('changed-English','manuscript',lambda v:v['records'][0].update(english='{SPEAKER:A6}Hello.')),
        ('manual-break','manuscript',lambda v:v['records'][0].update(english=v['records'][0]['english']+'{LB}')),
        ('manual-padding','manuscript',lambda v:v['records'][0].update(english=v['records'][0]['english']+'{PAD}')),
        ('FE-as-progressive','manuscript',lambda v:next(r for r in v['records'] if r['source_selector']==254).update(kind='progressive')),
        ('FE-static-identity','manuscript',lambda v:next(r for r in v['records'] if r['source_selector']==254).update(native_display_consumer='original_progressive_54020')),
        ('lost-retention-reason','manuscript',lambda v:next(r for r in v['records'] if r['editorial_decision']=='retain-wording').update(fresh_retained_wording_justification='')),
        ('lost-actual-scope','manuscript',lambda v:v['records'][0].update(actual_B22_display_fixture_observed=False)),
        ('missing-single-end','reference_map',lambda v:v['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong-single-end-map','reference_map',lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=398)),
        ('invented-relative','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'].append({})),
        ('invented-pause','reference_map',lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].append({})),
        ('invented-typed-object','reference_map',lambda v:v['blocks'][0]['choice_commands'].append({})),
        ('wrong-stored-offset','reference_map',lambda v:v['blocks'][0]['text_records'][0].update(new_offset=1)),
        ('wrong-stored-index','reference_map',lambda v:v['blocks'][0]['text_records'][0].update(new_record_index=1)),
        ('wrong-parity','reference_map',lambda v:v['blocks'][0]['text_records'][0].update(parity_space_added=not v['blocks'][0]['text_records'][0]['parity_space_added'])),
        ('wrong-target-block','reference_map',lambda v:v['blocks'][0].update(target_block_sha256='0'*64)),
        ('missing-command','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'].pop()),
        ('wrong-A000-boundary','reference_map',lambda v:next(r for r in v['blocks'][0]['mapped_native_commands'] if r['word']==0xA000).update(new_offset=10)),
        ('wrong-native-first-glyph','native_font_proof',lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('wrong-native-bounds','native_font_proof',lambda v:v['cases'][0].update(all_visible_origins_zero_and_within_four_rows=False)),
        ('lost-native-page','native_font_proof',lambda v:v['cases'][0].update(one_native_page_consumes_complete_target=False)),
        ('missing-native-case','native_font_proof',lambda v:v['cases'].pop()),
        ('false-native-negative','native_font_proof',lambda v:v['source_bound_formatter_negatives'][0].update(rejected=False)),
        ('missing-native-alignment','native_font_proof',lambda v:v['cases'][0]['current_native_macro_pipelines'][0]['cases'].pop()),
        ('FE-not-null','native_font_proof',lambda v:next(r for r in v['cases'] if r['kind']=='system-FE')['current_native_macro_pipelines'][0]['cases'][0].update(null_source_actor=False)),
        ('stored-cases-missing','final_padding_proof',lambda v:v['final_target_parity_cases'].pop()),
        ('wrong-stored-fresh-count','final_padding_proof',lambda v:v.update(new_parity_macro_alignment_cases=64)),
        ('wrong-FE-dispatch-actor','relocated_control_proof',lambda v:next(r for r in v['relocated_dispatch_cases'] if r['source_selector']==254).update(resolved_actor_ID=202)),
        ('missing-C200','relocated_control_proof',lambda v:v['relocated_C200_pairs'].pop()),
        ('wrong-C200-request','relocated_control_proof',lambda v:v['relocated_C200_pairs'][0]['cases'][1].update(source_owned_UI_request_words=[1,0,14,0,0,0,1])),
        ('lost-C200-memory-guard','relocated_control_proof',lambda v:v['relocated_C200_pairs'][0]['cases'][1].update(all_other4MiB_actor_roster_event_RNG_and_models_exact=False)),
        ('wrong-C200-offset','relocated_control_proof',lambda v:v['relocated_C200_pairs'][0].update(target_offset=400)),
        ('lost-A000-uninterpreted-scope','relocated_control_proof',lambda v:v.update(source_A000_packed_operand_semantics_not_inferred=False)),
        ('missing-end-decode','termination_decode_proof',lambda v:v['cases'].pop()),
        ('read-after-payload','termination_decode_proof',lambda v:v['cases'][0].update(post_logical_payload_reads=[{}])),
        ('wrong-Owner-role','source_nameplate_consumer_proof',lambda v:v['approved_prose_names'].update({'166':'Queen'})),
        ('wrong-Cook-catalogue','source_nameplate_consumer_proof',lambda v:v['full_catalogue_values'].update({'167':'Chef'})),
        ('invented-readonly-scratch','source_nameplate_consumer_proof',lambda v:next(r for r in v['native_six_consumer_cases']['rows'] if r['actor_ID']==166).update(original_scratch_rings=[{}])),
        ('invented-readonly-writes','source_nameplate_consumer_proof',lambda v:next(r for r in v['native_six_consumer_cases']['rows'] if r['actor_ID']==167).update(original_getter_writes=[{}])),
        ('natural-event-claim','representative_proof',lambda v:v.update(actual_selected_B178_source_events=[178])),
        ('missing-actual-ID','representative_proof',lambda v:v['actual_sampled_display_IDs'].pop()),
        ('missing-representative-approval','representative_proof',lambda v:v.update(actual_two_disclosed_content_cold_boots_pass=False)),
        ('wrong-nontext-count','postscene_native_state_proof',lambda v:v.update(nontext_equal_samples=114)),
        ('lost-final-RGB-equality','postscene_native_state_proof',lambda v:v.update(whole_RGB_final9001_equal=False)),
        ('lost-native-state-equality','postscene_native_state_proof',lambda v:v['postscene9001_native_component_equality'].update(state=False)),
        ('lost-actual-source-control-scope','postscene_native_state_proof',lambda v:v.update(source_A0008_C200488_single_end490_actually_executed=False)),
        ('wrong-timing-scope','postscene_native_state_proof',lambda v:v['actual_timing_differences'].append({})),
    ]
    mutations.extend(('missing-approval-'+flag,'reference_map',lambda v,f=flag:v.update({f:False})) for flag in owned.FLAGS)
    for m in ['FI','FA','FO']:
        mutations.append(('invented-macro-'+m,'manuscript',lambda v,m=m:v['records'][0].update(english=v['records'][0]['english']+' {MACRO:'+m+'}')))
    mutations.extend([
        ('missing-A000-structural-pair','relocated_control_proof',lambda v:v['relocated_A000_structural_pairs'].pop()),
        ('lost-future-world-limit','postscene_native_state_proof',lambda v:v.update(future_world_equivalence_and_full_RAM_equality_not_claimed=False)),
        ('wrong-PRNG-scope','postscene_native_state_proof',lambda v:v.update(postscene9001_PRNG_seeds=[0,0])),
    ])
    mutations.extend([
        ('hidden-indicator-difference','postscene_native_state_proof',lambda v:v['sampled_postscene_whole_RGB_differences_unmasked'].pop()),
        ('wrong-indicator-frame','postscene_native_state_proof',lambda v:v['sampled_postscene_whole_RGB_differences_unmasked'][0].update(frame=6011)),
        ('wrong-indicator-bounds','postscene_native_state_proof',lambda v:v['sampled_postscene_whole_RGB_differences_unmasked'][0].update(whole_frame_difference_bbox=[0,0,256,384])),
        ('invented-indicator-equality','postscene_native_state_proof',lambda v:v['sampled_postscene_whole_RGB_differences_unmasked'][0].update(whole_RGB_equal=True)),
        ('lost-indicator-visual-scope','postscene_native_state_proof',lambda v:v.update(all_four_following_indicator_differences_viewed_in_full_and_retained=False)),
        ('lost-PRNG-equality','postscene_native_state_proof',lambda v:v.update(PRNG_equality=False)),
        ('invented-PRNG-causal-trace','postscene_native_state_proof',lambda v:v.update(no_new_PRNG_causal_trace=False)),
        ('wrong-timing-counts','postscene_native_state_proof',lambda v:v['exact_timing_difference_counts'].update(speech=8)),
        ('wrong-exact-timing','postscene_native_state_proof',lambda v:v['actual_timing_differences'][0]['source'].update(returned=3335)),
        ('lost-fourth-fullscreen-sheet','postscene_native_state_proof',lambda v:v['paired_full_screen_views'].pop()),
        ('lost-town-RGB-equality','postscene_native_state_proof',lambda v:v.update(sampled_postscene_whole_RGB_equal_except_four_original_A_indicator_frames=False)),
    ])
    mutations.extend([
        ('wrong-third-Lady-name','source_nameplate_consumer_proof',lambda v:v['full_catalogue_values'].update({'168':'Duchess'})),
        ('missing-sixth-name-consumer','source_nameplate_consumer_proof',lambda v:v['native_six_consumer_cases']['rows'].pop()),
        ('missing-final-calendar-component','postscene_native_state_proof',lambda v:v['postscene9001_native_component_equality'].pop('calendar')),
    ])
    for label,key,edit in mutations:
        path=str(DOC) if key=='manuscript' else str(MAP) if key=='reference_map' else doc[key]
        value=deepcopy(read(path));initial=deepcopy(value);edit(value);assert value!=initial,label;reject(label,positive,{str(Path(path)):value})
    actual_path=next(p for p in sample['evidence'] if p.endswith('actual_all13_progressive_FE_A000_C200_and_single_end.json'))
    for label,edit in [
        ('missing-actual-version',lambda v:v['versions'].pop()),
        ('wrong-actual-single-end',lambda v:v['versions'][0]['selected_B22_command_pairs'][-1].update(original_source_offset=400)),
        ('lost-actual-C200-result',lambda v:v['versions'][0]['source_C200'].update(result_words=[3,1])),
        ('lost-actual-FE-count',lambda v:next(r for r in v['versions'][0]['selected_intervals'] if r['prefix']==254).update(prefix=2)),
        ('wrong-actual-A000-word',lambda v:v['versions'][0]['source_A000'][0].update(word=0xA001)),
        ('wrong-actual-A000-extent',lambda v:v['versions'][0]['source_A000'][0].update(extent=7)),
        ('false-actual-claim',lambda v:v.update(complete_matching_observations=9)),
    ]:
        value=deepcopy(read(actual_path));initial=deepcopy(value);edit(value);assert value!=initial,label;reject(label,positive,{str(Path(actual_path)):value})
    save(ROOT/'negative_cases.json',dict(cases=negatives,all_rejected_before_any_image_mutation=True,producer_sha256=sha(Path(__file__).read_bytes())))
    stage=b'''    lil_proof = profile_config.get('lil_B178_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B178_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B178_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B178 must run once after the complete V4655 stack')
        release_batches.append(more_batch)

'''
    anchor=b'    # Lexically valid "% o"'
    assert before.count(anchor)==1 and b"profile_config.get('lil_B178_editorial')" not in before
    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')
    assert [n.module for n in ast.walk(ast.parse('if True:\n'+stage.decode())) if isinstance(n,ast.ImportFrom)]==[owned.__name__]
    save(ROOT/'builder_hook_AST_review.json',dict(import_module=owned.__name__,explicit_profile_field='lil_B178_editorial',
        after_full_V4655_before_literal_percent_safety=True,stage_sha256=sha(stage),all_unowned_builder_bytes_exact=True))
    save(ROOT/'release_stack.before.json',registry);(ROOT/'build_integrated_release.py.before').write_bytes(before)
    save(owned.CONFIG,conf);profile=deepcopy(registry['profiles']['all-routes-unified-v4655'])
    profile.update(status='experimental',lil_B178_editorial=owned.CONFIG,
        description='Full V4655 stack plus thirteen B178 whole-exchange reviews:two revisions/eleven justified retentions,twelve progressive/one impersonal FE,three static Lady actors,six read-only names,no macros,16 commands,opaque A000,C200,single end. Paired9001-frame content boots display all thirteen panels and resume the original parent. All115 upper/portrait/name regions,five state components,whole actor/captain2,PRNG3306586022 and final RGB agree;14 command timings/four original A-indicator RGB differences remain disclosed.',
        note='Source/native/reference/representative approved;registered build,exact patch and current startup pending.')
    registry['profiles'][PROFILE]=profile
    assert rp.read_bytes()==raw and builder.read_bytes()==before
    temporary=builder.with_name('build_integrated_release_v4700.tmp');assert not temporary.exists();temporary.write_bytes(after);os.replace(temporary,builder)
    data=(json.dumps(registry,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    with rp.open('r+b') as stream:stream.write(data);stream.truncate(len(data));stream.flush();os.fsync(stream.fileno())
    check=deepcopy(read(rp));check['profiles'].pop(PROFILE)
    assert check==read(ROOT/'release_stack.before.json') and builder.read_bytes().replace(stage,b'',1)==before
    save(ROOT/'registration_receipt.json',dict(profile=PROFILE,parent_profile='all-routes-unified-v4655',parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        release_config=owned.CONFIG,release_config_sha256=sha(Path(owned.CONFIG).read_bytes()),manuscripts={str(DOC):sha(DOC.read_bytes())},
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),registry_before_sha256=sha(raw),registry_after_sha256=sha(rp.read_bytes()),
        builder_before_sha256=sha(before),builder_after_sha256=sha(builder.read_bytes()),positive_proof=str(ROOT/'positive_reconstruction.json'),
        negative_cases=str(ROOT/'negative_cases.json'),negative_count=len(negatives),all_negatives_reject_before_mutation=True,
        expected_manifest_batches=554,accepted_layers=114,promoted_profile_unchanged='all-routes-unified-v4595',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(registered=PROFILE,positive_records=13,negative_cases=len(negatives),expected_batches=554,accepted=114,promotion_unchanged=True))
