"""Register complete V1105 ancestry plus33 reviewed duel/escape paragraphs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch import sighting_grammar_editorial as parent
from dk4tool.patch import duel_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_release_v1165')
MANUSCRIPT = Path('translations/duel_editorial_manuscript_v4.json')
PROFILE = 'all-routes-unified-v1166'


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    registry_path, builder = Path('translations/release_stack.json'), Path('scripts/build_integrated_release.py')
    registry, raw, before = read(registry_path), registry_path.read_bytes(), builder.read_bytes()
    assert PROFILE not in registry['profiles']
    assert 'duel_editorial' not in registry['profiles']['all-routes-unified-v1105']
    doc = read(MANUSCRIPT)
    source = NdsImage.open(doc['current_ROM'])
    c, a, proof = owned.plan(source.read_file('/COMMON/MESFILE.DK4'), source.read_file('/__arm9__.bin'), doc)
    native_path = Path('work/analysis/duel_final_consumer_v1164/native_consumer_verification.json')
    copies_path = Path('work/analysis/duel_cache_copies_v1163/all_native_copies_and_prefix_cache_sequence.json')
    native, copies = read(native_path), read(copies_path)
    assert sha(c) == native['COMMON_sha256'] == copies['COMMON_sha256']
    assert sha(a) == native['ARM9_sha256'] == copies['ARM9_sha256']
    assert native['all53_exact_original_filters_and36_complete_final_native_font_cases_pass']
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    previous = read(parent.CONFIG)
    for name, digest in previous['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1 and b"profile_config.get('duel_editorial')" not in before
    lo = before.index(b"    sighting_grammar_editorial = profile_config.get('sighting_grammar_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'sighting_grammar', b'duel').replace(b'SIGHTING_GRAMMAR', b'DUEL')
    old_label = b"changed_records.setdefault(arm_path, []).append('DUEL_NATIVE_SELECTION_METADATA')"
    new_label = b"changed_records.setdefault(arm_path, []).extend(['DUEL_NATIVE_SELECTION_METADATA', 'DUEL_OWNED_RENDERER_AND_ESCAPE_SCOPE'])"
    assert block.count(old_label) == 1
    block = block.replace(old_label, new_label)
    after = before[:hi]+block+before[hi:]
    assert after.replace(block, b'', 1) == before
    compile(after, str(builder), 'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'repack_plan.json', proof)
    (ROOT/'target_COMMON.bin').write_bytes(c)
    (ROOT/'target_ARM9.bin').write_bytes(a)
    audit = ROOT/'native_audit/audit.json'
    audit.parent.mkdir()
    save(audit, {'batch': str(MANUSCRIPT), 'batch_sha256': sha(MANUSCRIPT.read_bytes()), 'records': doc['records'],
        'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a),
        'native_repack_plan': proof, 'final_native_consumer_proof': str(native_path),
        'final_native_consumer_proof_sha256': sha(native_path.read_bytes()),
        'complete_duel_font_cases': 1356, 'complete_escape_font_cases': 1417,
        'final53_selector_and36_complete_font_bindings': True,
        'reviewed_native_boundary_warnings': [read(doc['visual_review'])['contextual_weak_word_warning_retained']],
        'all33_source_glosses_and_prose_exact_to_v3': True,
        'blocking_errors': 0, 'unwaived_warnings': 0,
        'standard_story_audit_format_unsupported_COMMON_native_consumer_audit_used': True,
        'actual_registered_ROM_cache_visibility_duel_UI_and_transitions_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    extras = [str(Path(__file__)), str(MANUSCRIPT), str(audit), str(native_path), str(copies_path), parent.CONFIG,
        'dk4tool/patch/duel_editorial.py', str(owned.COMPONENT),
        'scripts/duel_editorial_layout_v1155.py', 'scripts/duel_escape_runtime_v1152.py',
        'scripts/duel_cache_front_v1142.py', 'scripts/duel_renderer_thumb_v1124.py',
        'scripts/duel_layout_native_v1141.c', 'scripts/duel_layout_native_v1141.ld',
        'scripts/prepare_duel_native_release_v1162.py', 'scripts/verify_duel_cache_copies_v1163.py',
        'scripts/verify_duel_final_consumer_v1164.py',
        'work/analysis/duel_layout_native_v1141b/compiler_provenance.json',
        'work/analysis/duel_native_ISA_v1160b/exact_binary_ISA_and_reproduction.json',
        'work/analysis/duel_PIC_positions_v1143/PIC_native_position_matrix.json']
    keys = ('native_context_proof', 'source_context_supplement', 'native_consumer_path_proof',
            'resident_font_proof', 'escape_font_proof', 'native_runtime_proof', 'visual_review', 'supersedes_manuscript')
    extras += [doc[key] for key in keys]
    extras += [row['path'] for row in read(doc['visual_review'])['all_six_sheets_visually_inspected']]
    checkpoint = read('work/analysis/duel_resident_checkpoint_v1161/checkpoint.json')
    extras += [v['path'] for v in checkpoint['completed_proofs'].values()]
    dependencies = {name: sha(Path(name).read_bytes()) for name in dict.fromkeys([*previous['dependencies'], *extras])}
    config = {'format': 'dk4-duel-editorial-v1', 'source_common_sha256': owned.SOURCE_COMMON,
        'source_arm9_sha256': owned.SOURCE_ARM, 'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
        'directory_sha256': proof['directory_sha256'], 'manuscript': str(MANUSCRIPT),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'native_copy_proof': str(copies_path),
        'native_consumer_audit': str(audit), 'dependencies': dependencies}
    save(owned.CONFIG, config)
    assert owned.apply_release(source.read_file('/COMMON/MESFILE.DK4'), source.read_file('/__arm9__.bin'), owned.CONFIG)[:2] == (c, a)
    assert registry_path.read_bytes() == raw and builder.read_bytes() == before
    (ROOT/'registry_before_raw.json').write_bytes(raw)
    save(ROOT/'registry_before.json', registry)
    (ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    builder.write_bytes(after)
    profile = deepcopy(registry['profiles']['all-routes-unified-v1105'])
    profile.update(duel_editorial=owned.CONFIG, status='experimental',
        description='Full V1105 stack plus33 source-reviewed duel/escape paragraphs and scoped existing-cache native layout.',
        note='Natural-dialogue-v2;1356 duel/1417 escape native fonts;7336 copies180 sequences;final53 caller36 font bindings. Existing allocations only;original duel UI/cache visibility/dismissal/transitions and cold boot/exact patch pending. Canonical unchanged.')
    registry['profiles'][PROFILE] = profile
    save(registry_path, registry)
    save(ROOT/'registration_provenance.json', {'builder_before_sha256': sha(before), 'builder_after_sha256': sha(after),
        'prior_builder_restored_by_removing_exact_optional_block': True,
        'registry_before_sha256': sha(raw), 'registry_after_sha256': sha(registry_path.read_bytes()),
        'accepted_layers_and_all_previous_profiles_preserved': True,
        'profile': PROFILE, 'source_profile': 'all-routes-unified-v1105',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'build_exact_patch_and_original_scenes_pending': True})
    print('V1166 experimental combined profile registered; final33 payload/all copies/native bindings pass. Build pending.', flush=True)


if __name__ == '__main__':
    main()
