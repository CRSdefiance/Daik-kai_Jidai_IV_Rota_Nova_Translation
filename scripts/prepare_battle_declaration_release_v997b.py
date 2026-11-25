"""Register22 macro-safe speech paragraphs after the complete V987 integrated stack."""
from copy import deepcopy
from pathlib import Path

from dk4tool.patch import activity_special_editorial_v987b as parent
from dk4tool.patch import battle_declaration_editorial as owned
from dk4tool.patch.common_single_cache_v861 import entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_declaration_layout_v996 import compiled
from scripts.probe_common_single_cache_v862 import Loader
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v997b')
MANUSCRIPT = Path('translations/battle_declaration_editorial_manuscript_v3.json')
OLD = Path('out/all_routes_combined_v987_candidate.nds')


def main():
    assert not ROOT.exists() and not Path(owned.CONFIG).exists()
    registry_path, builder = Path('translations/release_stack.json'), Path('scripts/build_integrated_release.py')
    registry, registry_raw, before = read(registry_path), registry_path.read_bytes(), builder.read_bytes()
    assert 'all-routes-unified-v997' not in registry['profiles']
    assert 'battle_declaration_editorial' not in registry['profiles']['all-routes-unified-v987']
    rom = NdsImage.open(OLD)
    doc, font, visual = [read(p) for p in (MANUSCRIPT, 'work/analysis/battle_declaration_v995b/native_font_proof.json', 'work/analysis/battle_declaration_v996/visual_review.json')]
    assert sha(OLD.read_bytes()) == doc['current_ROM_sha256']
    assert visual['all176_complete_previews_visually_reviewed_via8_full_canvas_sheets']
    c, a, proof = owned.plan(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), doc)
    for row in doc['records']:
        assert compiled(row).hex() == font['generated_paragraph_templates'][str(row['message_id'])]['compiled_hex']
    previous = read(parent.CONFIG)
    for name, digest in previous['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    anchor = b'    # Lexically valid "% o"'
    assert before.count(anchor) == 1 and b"profile_config.get('battle_declaration_editorial')" not in before
    lo = before.index(b"    activity_special_editorial = profile_config.get('activity_special_editorial')")
    hi = before.index(anchor)
    block = before[lo:hi].replace(b'activity_special', b'battle_declaration').replace(b'ACTIVITY_SPECIAL', b'BATTLE_DECLARATION')
    block = block.replace(b'battle_declaration_editorial_v987b', b'battle_declaration_editorial')
    after = before[:hi]+block+before[hi:]
    assert after.replace(block, b'', 1) == before
    compile(after, str(builder), 'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'repack_plan.json', proof)
    (ROOT/'target_COMMON.bin').write_bytes(c)
    (ROOT/'target_ARM9.bin').write_bytes(a)
    audit = ROOT/'native_audit/audit.json'
    audit.parent.mkdir()
    save(audit, {'batch': str(MANUSCRIPT), 'batch_sha256': sha(MANUSCRIPT.read_bytes()),
        'records': doc['records'], 'target_COMMON_sha256': sha(c), 'target_ARM9_sha256': sha(a),
        'native_repack_plan': proof, 'complete_native_font_cases': 176,
        'exact_real_name_matrix_cases': 140, 'synthetic_stress_cases': 21,
        'reviewed_native_boundary_warnings': visual['all27_line_boundary_findings'],
        'all176_complete_previews_visually_reviewed': True, 'blocking_errors': 0, 'unwaived_warnings': 0,
        'standard_story_audit_format_unsupported_COMMON_native_consumer_audit_used': True,
        'scope': 'Native source argument/speaker/branch proofs,complete fonts and exact post-expansion layout. Actual UI,registered ROM and scene transitions still pending.',
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    rows = entries(c, a, proof['directory_sha256'])
    loader, cases = Loader(a, c), []
    for mode in ('warm', 'cold'):
        for i, row in enumerate(rows):
            cases.append(loader.copy(row.message_id, row.text, mode))
            if (i+1) % 1000 == 0:
                print(mode, i+1, 'complete native copies', flush=True)
    loader.reset()
    sequence = []
    for block_id in list(range(41))+list(reversed(range(41)))+[0, 20, 0, 20, 40, 0, 40]:
        n = loader.directory[block_id][0]
        for _ in range(2):
            sequence.append(loader.copy(n, rows[n].text, 'sequence'))
    assert len(cases) == 7336 and len(sequence) == 178
    assert all(case['reads'] == 0 for case in sequence[1::2])
    copies = ROOT/'native_copy_proof.json'
    save(copies, {'COMMON_sha256': sha(c), 'ARM9_sha256': sha(a), 'complete_native_copies': len(cases), 'cases': cases,
        'sequenced_cache_cases': sequence, 'all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass': True,
        'callee_saved_ABI_and_stack_pass': True, 'existing_single_cache_policy_bytes_unchanged': True,
        'host_open_read_contract_only_not_actual_ROM_or_hardware': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    extra = ['dk4tool/patch/battle_declaration_editorial.py', parent.CONFIG,
        'scripts/battle_declaration_runtime_v993b.py', 'scripts/battle_declaration_layout_v996.py',
        'scripts/prepare_battle_declaration_release_v997b.py', 'scripts/prepare_battle_declaration_release_v997.py',
        'work/analysis/battle_declaration_v997/successor_provenance.json', 'scripts/research_battle_declaration_context_v991c.py',
        'scripts/prepare_battle_declaration_prose_v992.py', 'scripts/refine_battle_declaration_prose_v994.py',
        'scripts/verify_battle_declaration_runtime_v993b.py', 'scripts/finish_battle_declaration_runtime_v993c.py',
        'scripts/probe_battle_declaration_fonts_v995b.py', 'scripts/prepare_battle_declaration_native_v996.py',
        'translations/battle_declaration_editorial_manuscript_v1.json',
        'translations/battle_declaration_editorial_manuscript_v2.json',
        'work/analysis/battle_declaration_v990/source_inventory.json',
        'work/analysis/battle_declaration_v991c/source_context_packet.json',
        'work/analysis/battle_declaration_v992/source_context_and_faithfulness_review.json',
        'work/analysis/battle_declaration_v994/native_name_preview_followup.json',
        'work/analysis/battle_declaration_v993c/native_runtime_verification.json',
        'work/analysis/battle_declaration_v995b/native_font_proof.json',
        'work/analysis/battle_declaration_v996/visual_review.json',
        'work/analysis/battle_declaration_v996/all176_review_sheet_manifest.json', str(audit), str(copies)]
    extra += list(read('work/analysis/battle_declaration_v993c/native_runtime_verification.json')['all_completed_source_proofs'])
    dependencies = {name: sha(Path(name).read_bytes()) for name in dict.fromkeys([*previous['dependencies'], *extra])}
    config = {'format': 'dk4-battle-declaration-editorial-v1', 'source_common_sha256': owned.SOURCE_COMMON,
        'source_arm9_sha256': owned.SOURCE_ARM, 'target_common_sha256': sha(c), 'target_arm9_sha256': sha(a),
        'directory_sha256': proof['directory_sha256'], 'manuscript': str(MANUSCRIPT),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'native_copy_proof': str(copies),
        'native_consumer_audit': str(audit), 'dependencies': dependencies}
    save(owned.CONFIG, config)
    assert owned.apply_release(rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin'), owned.CONFIG)[:2] == (c, a)
    assert registry_path.read_bytes() == registry_raw and builder.read_bytes() == before
    save(ROOT/'registry_before.json', registry)
    (ROOT/'registry_before_raw.json').write_bytes(registry_raw)
    (ROOT/'builder_before.py').write_bytes(before)
    (ROOT/'builder_added_optional_stage.bin').write_bytes(block)
    builder.write_bytes(after)
    profile = deepcopy(registry['profiles']['all-routes-unified-v987'])
    profile.update(battle_declaration_editorial=owned.CONFIG, status='experimental',
        description='Complete V987 stack plus22 reviewed battle/declaration alternatives1889-1910.',
        note='Natural-dialogue-v2 paragraphs;832 original voice selections,45 wrapper and24 branch controls;176 complete font cases;7336 copies178 cache cases. Preserve complete faction names,source macros and fixed212/128-byte runtime spans. Actual UI/choices/dismissal/return,startup and exact patch pending;canonical unchanged.')
    registry['profiles']['all-routes-unified-v997'] = profile
    save(registry_path, registry)
    save(ROOT/'registration_provenance.json', {'builder_before_sha256': sha(before), 'builder_after_sha256': sha(after),
        'prior_builder_bytes_restored_by_removing_exact_added_block': after.replace(block, b'', 1) == before,
        'registry_before_raw_sha256': sha(registry_raw), 'registry_after_sha256': sha(registry_path.read_bytes()),
        'accepted_layers_and_canonical_baseline_preserved': True, 'full_stage_replay_matches_native_targets': True,
        'source_and_target_candidate_profiles': ['all-routes-unified-v987', 'all-routes-unified-v997'],
        'producer_sha256': sha(Path(__file__).read_bytes()), 'registered_ROM_actual_scenes_and_exact_patch_pending': True})
    print('V997 registered after all7336 native copies and178 cache cases;all22 paragraphs176 fonts. Build,actual scenes and exact patch remain pending.', flush=True)


if __name__ == '__main__':
    main()
