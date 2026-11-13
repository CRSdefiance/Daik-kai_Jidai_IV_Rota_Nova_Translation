"""Test atomic rejection contracts, then register one cumulative B170 release stage."""
import ast
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import lil_B170_editorial_v1 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B170_registration_v4302')
PROFILE = 'all-routes-unified-v4303'
PARENT = Path('out/all_routes_combined_v4251_candidate.nds')
DOC = Path('translations/lil_B170_editorial_manuscript_v6.json')
MAP = Path('translations/lil_B170_editorial_relocation_map_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    rp, builder = Path('translations/release_stack.json'), Path('scripts/build_integrated_release.py')
    raw, before = rp.read_bytes(), builder.read_bytes()
    registry = read(rp)
    prior = read('work/analysis/lil_B170_reference_checkpoint_v4299/checkpoint_receipt.json')['preserved_release_files']
    assert sha(raw) == prior[rp.as_posix()] and sha(before) == prior[builder.as_posix()]
    assert PROFILE not in registry['profiles'] and len(registry['accepted_layers']) == 114
    assert registry['latest_promoted_build']['profile'] == 'all-routes-unified-v4251'
    doc, mapping = read(DOC), read(MAP)
    parent, baseline = NdsImage.open(PARENT), NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(PARENT.read_bytes()) == doc['current_ROM_sha256']
    deps = {str(DOC), str(MAP), str(Path(owned.__file__).relative_to(Path.cwd())), str(Path(__file__).relative_to(Path.cwd())),
        'dk4tool/dialogue/lil_B170_layout_v2.py', 'dk4tool/dialogue/lil_B170_profile.py', 'dk4tool/dialogue/layout.py',
        'dk4tool/dialogue/encoder.py', 'dk4tool/dialogue/qa.py', 'dk4tool/dialogue/review.py',
        'docs/editorial_testing_scope_v1870.md', 'work/analysis/lil_B170_reference_approval_v4298/approval_receipt.json',
        'work/analysis/lil_B170_loader_v4285/whole_SC2_and_B170_initial_entry_proof.json'}
    deps.update(doc[key] for key in ['source_context', 'native_font_proof', 'native_progressive_proof', 'source_nameplate_consumer_proof',
        'final_padding_proof', 'relocated_control_proof', 'representative_proof', 'termination_decode_proof', 'actor_voice_contract',
        'effective_current_comparison', 'whole_exchange_context_notes', 'branch_proof', 'source_entry_proof', 'control_contract',
        'actor_terminology_reconciliation', 'source_effect_and_predicate_contract'])
    deps.update(mapping[key] for key in ['source_plan', 'source_census'])
    deps.add(doc['focused_repeat_proof'])
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
        for key in ['evidence', 'dependencies']:
            if not isinstance(value.get(key), dict):
                continue
            for item in value[key]:
                if Path(item).is_file() and Path(item).resolve() not in excluded and item not in deps:
                    deps.add(item)
                    pending.append(item)
    native, sample = read(doc['native_font_proof']), read(doc['representative_proof'])
    visual = read('work/analysis/lil_B170_transition_review_v4297/all6_sheets_figure_pause_effect_C200_and_paired_return_review.json')
    deps.update(sheet['path'] for sheet in native['review_sheets'] + sample['viewed_actual_sheets'])
    deps.update(row['preview'] for row in native['cases'])
    deps.update(row['path'] for row in visual['English_full_screen_views'] + visual['Japanese_full_screen_views'])
    deps.update(row['path'] for row in visual['later_diagnostic_full_screen_views'])
    conf = dict(format='dk4-lil-B170-editorial-release-v1', manuscript=str(DOC), reference_map=str(MAP),
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
        ('missing_gate', 'manuscript', lambda value: value['records'][0]['review'].update(source=False)),
        ('missing_speech', 'manuscript', lambda value: value['records'].pop()),
        ('wrong_source', 'manuscript', lambda value: value['records'][0]['source_reference'].update(offset=1)),
        ('wrong_current', 'manuscript', lambda value: value['records'][0]['current_reference'].update(offset=1)),
        ('wrong_selector', 'manuscript', lambda value: value['records'][0].update(english='{SPEAKER:19}Hello.')),
        ('Yifa_selector_as_text', 'manuscript', lambda value: value['records'][1].update(english='Yifa says hello.')),
        ('manual_break', 'manuscript', lambda value: value['records'][0].update(english=value['records'][0]['english'] + '{LB}')),
        ('manual_padding', 'manuscript', lambda value: value['records'][0].update(english=value['records'][0]['english'] + '{PAD}')),
        ('invented_relative', 'reference_map', lambda value: value['blocks'][0]['relative_skip_fixups'].append({})),
        ('missing_pause', 'reference_map', lambda value: value['blocks'][0]['original2000_pause_and_resume_maps'].pop()),
        ('wrong_pause_resume', 'reference_map', lambda value: value['blocks'][0]['original2000_pause_and_resume_maps'][0].update(target_resume=36)),
        ('missing_end', 'reference_map', lambda value: value['blocks'][0]['original_declared_end_word_maps'].pop()),
        ('wrong_end', 'reference_map', lambda value: value['blocks'][0]['original_declared_end_word_maps'][0].update(target_offset=0)),
        ('wrong_entry', 'reference_map', lambda value: value.update(entry_point_offset=10)),
        ('invented_choice', 'reference_map', lambda value: value['blocks'][0]['choice_commands'].append({})),
        ('wrong_command', 'reference_map', lambda value: value['blocks'][0]['mapped_native_commands'][0].update(new_offset=10)),
        ('wrong_A000_raw_word', 'reference_map', lambda value: value.update(source_A000_raw_hex_words=['0029', '0001'])),
        ('missing_native_plane', 'native_font_proof', lambda value: value['cases'].pop()),
        ('lost_internal_glyph', 'native_font_proof', lambda value: value['cases'][0].update(all_first_final_internal_glyphs_in_order_and_unique_cells=False)),
        ('lost_native_bounds', 'native_font_proof', lambda value: value['cases'][0].update(all_visible_origins_zero_and16px_rows_within4rows=False)),
        ('lost_macro_negative', 'native_font_proof', lambda value: value['source_macro_preservation_negatives'].pop()),
        ('lost_stored_plane', 'final_padding_proof', lambda value: value['final_target_parity_cases'].pop()),
        ('lost_dispatch', 'relocated_control_proof', lambda value: value['relocated_dispatch_cases'].pop()),
        ('invented_predicate', 'relocated_control_proof', lambda value: value['relocated_predicate_pairs'].append({})),
        ('lost_C200', 'relocated_control_proof', lambda value: value['relocated_C200_pairs'].pop()),
        ('wrong_C200_ownership', 'relocated_control_proof', lambda value: value.update(original_C200_queue_and_all_unowned4MiB_preserved_at_relocated_cursor=False)),
        ('wrong_resource_reuse', 'relocated_control_proof', lambda value: value.update(source_resource20_boundary_cases_reused_only_by_exact_words_and_runtime=False)),
        ('lost_opaque_leaf', 'relocated_control_proof', lambda value: value['all12_source_current_target_nonrelative_nonspeech_leaves'].pop()),
        ('lost_name_path', 'source_nameplate_consumer_proof', lambda value: value['native_four_consumer_cases']['rows'].pop()),
        ('lost_owned_scratch', 'source_nameplate_consumer_proof', lambda value: value['native_four_consumer_cases']['rows'][0].update(original_scratch_rings=[])),
        ('lost_end_decode', 'termination_decode_proof', lambda value: value['cases'].pop()),
        ('post_payload_read', 'termination_decode_proof', lambda value: value.update(all4_declared_end_decodes_return_type0_extent4_without_post_payload_read=False)),
        ('false_actual_second_end', 'representative_proof', lambda value: value.update(first_end1852_actual_second1856_native_decoder_only=False)),
        ('omitted_effect', 'representative_proof', lambda value: value.update(no_B170_source_command_omitted=False)),
        ('invented_earned_effect', 'representative_proof', lambda value: value.update(source_A000_packed_semantics_or_earned_recruitment_not_inferred=False)),
        ('lost_later_difference_scope', 'representative_proof', lambda value: value.update(later67_SeaView_differences_preserved_with_explicit_inference_and_state_scope=False)),
        ('lost_repeat_actor_state', 'focused_repeat_proof', lambda value: value.update(paired_post_B170_town11290_whole1A04_actor_models_and_captain2_equal=False)),
        ('lost_repeat_component_state', 'focused_repeat_proof', lambda value: value['paired_native_persistent_state_and_PRNG_samples'][2]['component_equality'].update(models=False)),
        ('lost_timing_distinction', 'focused_repeat_proof', lambda value: value['cross_language_speech_timing_differences'].pop()),
    ]
    for macro in ['FI', 'FO']:
        def remove_macro(value, macro=macro):
            row = next(row for row in value['records'] if '{MACRO:' + macro + '}' in row['english'])
            row['english'] = row['english'].replace('{MACRO:' + macro + '}', 'Literal', 1)
        mutations.append(('missing_' + macro, 'manuscript', remove_macro))
    def changed_actual(value, label):
        old = next(path for path in value['evidence'] if path.endswith('actual_all33_pause_resources_A000_C200_and_first_end.json'))
        actual = read(old)
        if label == 'wrong_actual_effect':
            actual['versions'][0]['actual_source_A000_hex1019_2001']['result_words'] = [3, 1]
        elif label == 'wrong_actual_end':
            actual['versions'][0]['source_first_end_offset'] = 1856
        elif label == 'wrong_actual_C200':
            actual['versions'][0]['actual_C200']['result_words'] = [3, 1]
        elif label == 'wrong_actual_pause':
            actual['versions'][0]['actual_pause_and_resume'][0]['returned'] = 3333
        else:
            actual['versions'].pop()
        destination = ROOT / label / 'actual_all33_pause_resources_A000_C200_and_first_end.json'
        destination.parent.mkdir()
        save(destination, actual)
        value['evidence'].pop(old)
        value['evidence'][str(destination)] = sha(destination.read_bytes())
    mutations.extend((label, 'representative_proof', lambda value, label=label: changed_actual(value, label))
                     for label in ['wrong_actual_effect', 'wrong_actual_end', 'wrong_actual_C200', 'wrong_actual_pause', 'missing_actual_version'])
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
    stage = b'''    lil_proof = profile_config.get('lil_B170_editorial')
    if lil_proof:
        from dk4tool.patch.lil_B170_editorial_v1 import apply_release as apply_lil_proof

        lil_proof_report = apply_lil_proof(candidate, baseline, lil_proof)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_proof_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B170_editorial'] = {
            'release_config': lil_proof,
            'release_config_sha256': sha256(Path(lil_proof).read_bytes()),
            'proof': lil_proof_report}
        more_batch = Path(lil_proof_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B170 must run once after the complete V4251 stack')
        release_batches.append(more_batch)

'''
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1 and b"profile_config.get('lil_B170_editorial')" not in before
    after = before.replace(anchor, stage + anchor)
    compile(after, str(builder), 'exec')
    assert [node.module for node in ast.walk(ast.parse('if True:\n' + stage.decode())) if isinstance(node, ast.ImportFrom)] == [owned.__name__]
    save(ROOT / 'builder_hook_AST_review.json', dict(import_module=owned.__name__, explicit_profile_field='lil_B170_editorial',
        after_full_V4251_before_literal_percent_safety=True, stage_sha256=sha(stage), all_unowned_builder_bytes_exact=True))
    save(ROOT / 'release_stack.before.json', registry)
    (ROOT / 'build_integrated_release.py.before').write_bytes(before)
    save(owned.CONFIG, conf)
    profile = deepcopy(registry['profiles']['all-routes-unified-v4251'])
    profile.update(status='experimental', lil_B170_editorial=owned.CONFIG,
        description='Full V4251 cumulative stack plus33 complete B170 Yifa collision/apology/Taoist-training/resolve/passage reviews:21 revisions/12 retentions,33 progressive speeches,45 commands,twelve leaves,pause,resources,later A000 hex1019/2001,C200 and both ends. Two complete-content boots cover all33 panels,first end and normal return;two focused repeats bind original state and later PRNG/timing scope. No natural eligibility,earned flag,full-route orhardware claim.', note='B170 source/native/reference/representative approved;registered build,exact patch and fresh startup pending.')
    registry['profiles'][PROFILE] = profile
    assert rp.read_bytes() == raw and builder.read_bytes() == before
    temporary = builder.with_name('build_integrated_release_v4302.tmp')
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
    save(ROOT / 'registration_receipt.json', dict(profile=PROFILE, parent_profile='all-routes-unified-v4251',
        parent_ROM=str(PARENT), parent_ROM_sha256=sha(PARENT.read_bytes()), release_config=owned.CONFIG,
        release_config_sha256=sha(Path(owned.CONFIG).read_bytes()), manuscripts={str(DOC): sha(DOC.read_bytes())},
        reference_map=str(MAP), reference_map_sha256=sha(MAP.read_bytes()), registry_before_sha256=sha(raw), registry_after_sha256=sha(rp.read_bytes()),
        builder_before_sha256=sha(before), builder_after_sha256=sha(builder.read_bytes()), positive_proof=str(ROOT / 'positive_reconstruction.json'),
        negative_cases=str(ROOT / 'negative_cases.json'), negative_count=len(negatives), all_negatives_reject_before_mutation=True,
        expected_manifest_batches=546, accepted_layers=114, promoted_profile_unchanged='all-routes-unified-v4251',
        producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    print(dict(registered=PROFILE, positive_records=33, negative_cases=len(negatives), expected_batches=546, accepted=114, promotion_unchanged=True))
