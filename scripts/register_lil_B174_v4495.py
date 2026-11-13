"""Test atomic rejection contracts, then register one cumulative B174 release stage."""
import ast
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B174_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B174_registration_v4495')
PROFILE = 'all-routes-unified-v4496'
PARENT = Path('out/all_routes_combined_v4445_candidate.nds')
DOC = Path('translations/lil_B174_editorial_manuscript_v6.json')
MAP = Path('translations/lil_B174_editorial_relocation_map_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp, builder = Path('translations/release_stack.json'), Path('scripts/build_integrated_release.py')
    raw, before = rp.read_bytes(), builder.read_bytes()
    registry = read(rp)
    prior = read('work/analysis/lil_B174_reference_checkpoint_v4492/checkpoint_receipt.json')['preserved_release_files']
    assert sha(raw) == prior[rp.as_posix()] and sha(before) == prior[builder.as_posix()]
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4445'
    doc, mapping = read(DOC), read(MAP)
    parent, baseline = NdsImage.open(PARENT), NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256']
    deps = {str(DOC), str(MAP), str(Path(owned.__file__).relative_to(Path.cwd())), str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B174_layout_v2.py', 'dk4tool/dialogue/lil_B174_profile.py', 'dk4tool/dialogue/layout.py',
        'dk4tool/dialogue/encoder.py', 'dk4tool/dialogue/qa.py', 'dk4tool/dialogue/review.py',
        'docs/editorial_testing_scope_v1870.md', 'work/analysis/lil_B174_reference_approval_v4491/approval_receipt.json',
        'work/analysis/lil_B174_loader_v4483/whole_SC2_and_B174_initial_entry_proof.json',
        'work/analysis/editorial_handoff_verification_v4493/verified_handoff.json'}
    deps.update(doc[key] for key in ['source_context', 'native_font_proof', 'native_progressive_proof', 'source_nameplate_consumer_proof',
        'final_padding_proof', 'relocated_control_proof', 'representative_proof', 'termination_decode_proof', 'actor_voice_contract',
        'effective_current_comparison', 'whole_exchange_context_notes', 'branch_proof', 'source_entry_proof', 'control_contract',
        'actor_terminology_reconciliation', 'source_effect_and_predicate_contract'])
    deps.update(mapping[key] for key in ['source_plan', 'source_census'])
    deps.add(doc['postscene_native_state_proof'])
    excluded = {path.resolve() for path in [rp, builder, Path('translations/editorial_review_current_v1.json'),
        *[Path('docs') / name for name in ['editorial_handoff_current.md', 'translation_progress.md', 'editorial_review_goal.md', 'todo.md', 'known_issues.md']]]}
    pending, seen = list(deps), set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        if Path(path).suffix != '.json':
            continue
        value = read(path)
        if not isinstance(value, dict):
            continue
        for key in ['evidence', 'dependencies']:
            if not isinstance(value.get(key), dict):
                continue
            for item in value[key]:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:
                    deps.add(item)
                    pending.append(item)
    native, sample = read(doc['native_font_proof']), read(doc['representative_proof'])
    visual = read('work/analysis/lil_B174_actual_review_v4490b/all6_actual_sheets_optional_scope_join_notice_paired_return_and_final_state.json')
    deps.update(sheet['path'] for sheet in native['review_sheets'] + sample['viewed_actual_sheets'])
    deps.update(row['preview'] for row in native['cases'])
    deps.update(row['path'] for row in visual['paired_full_screen_views'])
    conf = dict(format='dk4-lil-B174-editorial-release-v1', manuscript=str(DOC), reference_map=str(MAP),
        required_runtime_arm9_sha256=sha(parent.read_file('/__arm9__.bin')), required_runtime_common_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        source_SC2_sha256=mapping['source_SC2_sha256'], target_SC2_sha256=mapping['target_SC2_sha256'],
        canonical_SC2_sha256=mapping['canonical_SC2_sha256'], clean_SC2_sha256=mapping['clean_SC2_sha256'],
        clean_ROM='work/clean.nds', clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        dependencies={path: sha(Path(path).read_bytes()) for path in sorted(deps)})
    ROOT.mkdir(parents=True)
    positive = ROOT / 'positive_config.json'
    save(positive, conf)
    test = NdsImage.open(PARENT)
    proof = owned.apply_release(test, baseline, positive)
    expected = Path(read(mapping['source_plan'])['target_SC2']).read_bytes()
    assert test.read_file(owned.PATH) == expected and len(proof['changed_records']) == 33
    save(ROOT / 'positive_reconstruction.json', proof)
    negatives = []
    def reject(label, config):
        image = NdsImage.open(PARENT)
        initial = [image.read_file(path) for path in [owned.PATH, '/__arm9__.bin', '/COMMON/MESFILE.DK4']]
        try:
            owned.apply_release(image, baseline, config)
        except (ValueError, AssertionError, KeyError) as error:
            negatives.append(dict(case=label, rejected=True, error=str(error)))
        else:
            raise AssertionError('Accepted negative:' + label)
        assert initial == [image.read_file(path) for path in [owned.PATH, '/__arm9__.bin', '/COMMON/MESFILE.DK4']], label
    for label, key, value in [('unknown_format', 'format', 'bad'), ('wrong_runtime', 'required_runtime_arm9_sha256', '0' * 64),
        ('wrong_COMMON', 'required_runtime_common_sha256', '0' * 64), ('wrong_source', 'source_SC2_sha256', '0' * 64),
        ('wrong_canonical', 'canonical_SC2_sha256', '0' * 64), ('wrong_clean_input', 'clean_ROM_sha256', '0' * 64),
        ('wrong_clean_script', 'clean_SC2_sha256', '0' * 64), ('wrong_target', 'target_SC2_sha256', '0' * 64)]:
        changed = deepcopy(conf)
        changed[key] = value
        path = ROOT / (label + '_config.json')
        save(path, changed)
        reject(label, path)
    changed = deepcopy(conf)
    changed['dependencies'][str(DOC)] = '0' * 64
    path = ROOT / 'bad_dependency_config.json'
    save(path, changed)
    reject('bad_dependency', path)
    mutations = [
        ('missing_gate','manuscript',lambda v:v['records'][0]['review'].update(source=False)),
        ('missing_speech','manuscript',lambda v:v['records'].pop()),
        ('wrong_source','manuscript',lambda v:v['records'][0]['source_reference'].update(offset=1)),
        ('wrong_current','manuscript',lambda v:v['records'][0]['current_reference'].update(offset=1)),
        ('wrong_selector','manuscript',lambda v:v['records'][0].update(english='{SPEAKER:02}Hello.')),
        ('Mihwa_selector_as_text','manuscript',lambda v:v['records'][1].update(english='Mihwa says hello.')),
        ('manual_break','manuscript',lambda v:v['records'][0].update(english=v['records'][0]['english']+'{LB}')),
        ('manual_padding','manuscript',lambda v:v['records'][0].update(english=v['records'][0]['english']+'{PAD}')),
        ('missing_relative','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'].pop()),
        ('wrong_relative_span','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(target_span=2)),
        ('wrong_relative_offset','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_offset=0)),
        ('wrong_relative_destination','reference_map',lambda v:v['blocks'][0]['relative_skip_fixups'][0].update(new_matched_skip_target=0)),
        ('missing_target_operand_case','reference_map',lambda v:v['blocks'][0]['target_native_skip_cases'].pop()),
        ('lost_relative_memory_guard','reference_map',lambda v:v['blocks'][0]['target_native_skip_cases'][0].update(ABI_all4MiB_owner_stream_result_length_and_guards_exact=False)),
        ('invented_pause','reference_map',lambda v:v['blocks'][0]['original2000_pause_and_resume_maps'].append({})),
        ('extra_A000','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'].append(dict(word=0xA000))),
        ('missing_end','reference_map',lambda v:v['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong_end','reference_map',lambda v:v['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=0)),
        ('wrong_entry','reference_map',lambda v:v.update(entry_point_offset=10)),
        ('invented_choice','reference_map',lambda v:v['blocks'][0]['choice_commands'].append({})),
        ('wrong_command','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_command_word','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'][0].update(word=0x6001)),
        ('wrong_resource_extent','reference_map',lambda v:v['blocks'][0]['mapped_native_commands'][1].update(old_native_extent=4)),
        ('missing_native_plane','native_font_proof',lambda v:v['cases'].pop()),
        ('lost_internal_glyph','native_font_proof',lambda v:v['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost_native_bounds','native_font_proof',lambda v:v['cases'][0].update(all_visible_origins_zero_and16px_rows_within4rows=False)),
        ('lost_macro_negative','native_font_proof',lambda v:v['source_macro_absence_negatives'].pop()),
        ('lost_stored_plane','final_padding_proof',lambda v:v['final_target_parity_cases'].pop()),
        ('lost_dispatch','relocated_control_proof',lambda v:v['relocated_dispatch_cases'].pop()),
        ('lost_predicate','relocated_control_proof',lambda v:v['relocated_predicate_pairs'].pop()),
        ('wrong_predicate_result','relocated_control_proof',lambda v:v['relocated_predicate_pairs'][0]['cases'][1].update(native_result=[2,0,0,0,0,0])),
        ('wrong_predicate_ownership','relocated_control_proof',lambda v:v.update(original_predicate_owned_operand_scratch_and_all_unowned4MiB_preserved_at_relocated_cursor=False)),
        ('wrong_resource_reuse','relocated_control_proof',lambda v:v.update(source_resource10_boundary_cases_reused_only_by_exact_words_and_runtime=False)),
        ('lost_opaque_leaf','relocated_control_proof',lambda v:v['all8_source_current_target_nonrelative_nonspeech_leaves'].pop()),
        ('lost_suffix_path','relocated_control_proof',lambda v:v['source_four_relative_sites20_relocated_operand_cases_and_both_boolean_suffix_paths'].pop()),
        ('lost_name_path','source_nameplate_consumer_proof',lambda v:v['native_eight_consumer_cases']['rows'].pop()),
        ('lost_owned_scratch','source_nameplate_consumer_proof',lambda v:v['native_eight_consumer_cases']['rows'][0].update(original_scratch_rings=[])),
        ('lost_end_decode','termination_decode_proof',lambda v:v['cases'].pop()),
        ('post_payload_read','termination_decode_proof',lambda v:v.update(all2_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('lost_actual_single_end','representative_proof',lambda v:v.update(single_end2086_actual=False)),
        ('omitted_effect','representative_proof',lambda v:v.update(no_B174_source_command_omitted=False)),
        ('invented_earned_effect','representative_proof',lambda v:v.update(no_natural_event_eligibility_earned_flags_full_route_or_hardware_claim=False)),
        ('lost_offline_jump_scope','representative_proof',lambda v:v.update(source_relative_sites882890_actual_886894938_offline_native_only=False)),
        ('lost_actual_VM_last_result_scope','representative_proof',lambda v:v.update(actual_VM_descriptor_last_result0_preserved_through_type3_C200_and_end=False)),
        ('lost_postscene_actor_state','postscene_native_state_proof',lambda v:v.update(postscene16001_whole1A04_actor_models_and_captain2_equal=False)),
        ('lost_postscene_component_state','postscene_native_state_proof',lambda v:v['postscene16001_native_component_equality'].update(models=False)),
        ('lost_timing_distinction','postscene_native_state_proof',lambda v:v['actual_timing_differences'].pop()),
        ('lost_PRNG_scope','postscene_native_state_proof',lambda v:v.update(PRNG_equality_or_future_world_equivalence_not_claimed=False)),
    ]
    mutations.extend([
        ('invented_actual_Emilio','manuscript',lambda v:next(r for r in v['records'] if r['source_record_index']==69).update(actual_B22_display_fixture_observed=True)),
        ('lost_Emilio_UI_boundary','manuscript',lambda v:next(r for r in v['records'] if r['source_record_index']==69).update(current_native_UI_body_explicit_unexecuted_boundary=False)),
        ('missing_C200_pair','relocated_control_proof',lambda v:v['relocated_C200_pairs'].pop()),
        ('wrong_C200_request','relocated_control_proof',lambda v:v['relocated_C200_pairs'][0]['cases'][1].update(source_owned_UI_request_words=[1,0,14,0,0,0,1])),
        ('wrong_C200_ownership','relocated_control_proof',lambda v:v['relocated_C200_pairs'][0]['cases'][1].update(all_other4MiB_actor_roster_event_RNG_and_models_exact=False)),
        ('lost_join_notice_first_J','postscene_native_state_proof',lambda v:v.update(join_notice_leading_J_full_Julian_Lopes_and_trailing_exclamation_viewed=False)),
        ('wrong_join_indicator_scope','postscene_native_state_proof',lambda v:v.update(join_notice_full_RGB_difference_is_original_A_button_indicator=[0,0,256,384])),
        ('lost_native_exact_reuse_scope','native_font_proof',lambda v:v.update(reused_original_macro_alignment_calls=0)),
    ])
    for macro in ['FI','FA','FO']:
        def invent_macro(value,macro=macro):
            value['records'][0]['english']+=' {MACRO:'+macro+'}'
        mutations.append(('invented_'+macro,'manuscript',invent_macro))
    mutations.extend([
        ('invented_Mihwa_scratch_write','source_nameplate_consumer_proof',lambda value:next(r for r in value['native_eight_consumer_cases']['rows'] if r['actor_ID']==201).update(original_getter_writes=[{}])),
        ('invented_Mihwa_scratch_ring','source_nameplate_consumer_proof',lambda value:next(r for r in value['native_eight_consumer_cases']['rows'] if r['actor_ID']==201).update(original_scratch_rings=[{}])),
    ])
    def changed_actual(value,label):
        old=next(p for p in value['evidence'] if p.endswith('actual_all33_unforced_predicate_paths_effects_C200_and_end.json'))
        actual=read(old);version=actual['versions'][0]
        if label=='wrong_actual_presentation':version['actual_presentation_commands'][0]['word']=0x6001
        elif label=='wrong_actual_end':version['single_source_end_offset']=2090
        elif label=='wrong_actual_predicate':version['actual_predicate']['result_words']=[2,1]
        elif label=='wrong_actual_A000':version['source_A000_hex_by_offset']['2076']='00a0ffff00000000'
        elif label=='invent_actual_effect_last_result':version['actual_source_A000s'][1]['result_words']=[3,1]
        elif label=='invent_actual_end_last_result':version['selected_B22_command_pairs'][-1]['result_words']=[0,1]
        elif label=='invent_actual_relative_last_result':version['actual_source_relative_commands'][0]['result_words']=[3,1]
        elif label=='wrong_actual_resource':version['actual_resources'][0]['word']=0x6326
        elif label=='wrong_actual_C200':version['actual_source_C200'][0]['result_words']=[3,1]
        elif label=='wrong_actual_skip_extent':version['actual_source_relative_commands'][1]['extent']+=2
        elif label=='missing_actual_offline_scope':actual['offline_only_display_IDs']=[]
        else:actual['versions'].pop()
        destination=ROOT/label/'actual_all33_unforced_predicate_paths_effects_C200_and_end.json';destination.parent.mkdir()
        save(destination,actual);value['evidence'].pop(old);value['evidence'][str(destination)]=sha(destination.read_bytes())
    mutations.extend((label,'representative_proof',lambda value,label=label:changed_actual(value,label)) for label in [
        'wrong_actual_presentation','wrong_actual_end','wrong_actual_predicate','wrong_actual_resource','wrong_actual_A000',
        'invent_actual_effect_last_result','invent_actual_end_last_result','invent_actual_relative_last_result','missing_actual_version', 'wrong_actual_C200','wrong_actual_skip_extent','missing_actual_offline_scope'])
    mutations.extend(('map_' + flag, 'reference_map', lambda value, flag=flag: value.update({flag: False})) for flag in owned.FLAGS)
    for label, key, edit in mutations:
        changed_doc, changed_map, changed_conf = deepcopy(doc), deepcopy(mapping), deepcopy(conf)
        if key in ['manuscript', 'reference_map']:
            edit({'manuscript': changed_doc, 'reference_map': changed_map}[key])
        else:
            value = read(doc[key])
            edit(value)
            destination = ROOT / (label + '_proof.json')
            save(destination, value)
            changed_doc[key] = str(destination)
            changed_doc[key + '_sha256'] = sha(destination.read_bytes())
            changed_conf['dependencies'][str(destination)] = sha(destination.read_bytes())
        map_path = ROOT / (label + '_map.json')
        save(map_path, changed_map)
        changed_doc['reference_map'], changed_doc['reference_map_sha256'] = str(map_path), sha(map_path.read_bytes())
        doc_path, config_path = ROOT / (label + '_manuscript.json'), ROOT / (label + '_config.json')
        save(doc_path, changed_doc)
        changed_conf.update(manuscript=str(doc_path), reference_map=str(map_path))
        changed_conf['dependencies'].update({str(path): sha(path.read_bytes()) for path in [map_path, doc_path]})
        save(config_path, changed_conf)
        reject(label, config_path)
    assert len(negatives) == 9 + len(mutations)
    save(ROOT / 'negative_cases.json', dict(cases=negatives, all_rejected_before_mutation=True))
    stage = b'''    lil_proof = profile_config.get('lil_B174_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B174_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B174_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B174 must run once after the complete V4445 stack')
        release_batches.append(more_batch)

'''
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1 and b"profile_config.get('lil_B174_editorial')" not in before
    after = before.replace(anchor, stage + anchor)
    compile(after, str(builder), 'exec')
    assert [node.module for node in ast.walk(ast.parse('if True:\n' + stage.decode())) if isinstance(node, ast.ImportFrom)] == [owned.__name__]
    save(ROOT / 'builder_hook_AST_review.json', dict(import_module=owned.__name__, explicit_profile_field='lil_B174_editorial',
        after_full_V4445_before_literal_percent_safety=True, stage_sha256=sha(stage), all_unowned_builder_bytes_exact=True))
    save(ROOT / 'release_stack.before.json', registry)
    (ROOT / 'build_integrated_release.py.before').write_bytes(before)
    save(owned.CONFIG, conf)
    profile = deepcopy(registry['profiles']['all-routes-unified-v4445'])
    profile.update(status='experimental',lil_B174_editorial=owned.CONFIG,
        description='Full V4445 cumulative stack plus33 B174 crown/grandfather-aspiration/conditional-date reviews:23 revisions/10 retentions,45 commands,eight numeric leaves,four relative sites/20 target cases,one predicate,two A000s and C200. Two16001-frame unforced content boots observe32 unconditional panels,result0,both effects,C200,single end andnormal town return;232 nontext regions match. Optional Emilio R69 retains offline native coverage. Actual source/target skip extents52/62 and VM last-result0 are explicit. Exported postscene state is compared without PRNG/future-world equality or natural eligibility claims.',
        note='B174 source/native/reference/representative approved;registered build,exact patch andfresh startup pending.')
    registry['profiles'][PROFILE] = profile
    assert rp.read_bytes() == raw and builder.read_bytes() == before
    temporary = builder.with_name('build_integrated_release_v4495.tmp')
    assert not temporary.exists()
    temporary.write_bytes(after)
    os.replace(temporary, builder)
    import json
    registry_bytes=(json.dumps(registry,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')
    assert len(registry_bytes)>len(raw)
    with rp.open('r+b') as stream:
        stream.write(registry_bytes)
        stream.flush()
        os.fsync(stream.fileno())
    check = deepcopy(read(rp))
    check['profiles'].pop(PROFILE)
    assert check == read(ROOT / 'release_stack.before.json') and builder.read_bytes().replace(stage, b'', 1) == before
    save(ROOT / 'registration_receipt.json', dict(profile=PROFILE, parent_profile='all-routes-unified-v4445',
        parent_ROM=str(PARENT), parent_ROM_sha256=sha(PARENT.read_bytes()), release_config=owned.CONFIG,
        release_config_sha256=sha(Path(owned.CONFIG).read_bytes()), manuscripts={str(DOC): sha(DOC.read_bytes())},
        reference_map=str(MAP), reference_map_sha256=sha(MAP.read_bytes()), registry_before_sha256=sha(raw), registry_after_sha256=sha(rp.read_bytes()),
        builder_before_sha256=sha(before), builder_after_sha256=sha(builder.read_bytes()), positive_proof=str(ROOT / 'positive_reconstruction.json'),
        negative_cases=str(ROOT / 'negative_cases.json'), negative_count=len(negatives), all_negatives_reject_before_mutation=True,
        expected_manifest_batches=550, accepted_layers=114, promoted_profile_unchanged='all-routes-unified-v4445',
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print(dict(registered=PROFILE, positive_records=33, negative_cases=len(negatives), expected_batches=550, accepted=114, promotion_unchanged=True))
