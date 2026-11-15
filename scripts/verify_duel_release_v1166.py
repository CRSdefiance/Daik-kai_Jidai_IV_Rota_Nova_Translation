"""Verify registered combined ancestry and an exact clean-input patch."""
from pathlib import Path
from dk4tool.patch import sighting_grammar_editorial as parent
from dk4tool.patch import duel_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta, apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.duel_editorial_layout_v1155 import IDS, compiled
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_release_v1165')
OLD = Path('out/all_routes_combined_v1105_candidate.nds')
ROM = Path('out/all_routes_combined_v1166_candidate.nds')


def main():
    proof_path = ROOT/'registered_release_verification.json'
    assert not proof_path.exists()
    registry, prior = read('translations/release_stack.json'), read(ROOT/'registry_before.json')
    manifest, previous = read(ROM.with_suffix('.manifest.json')), read(OLD.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v1166'
    assert manifest['base_rom'] == 'out\\raphael_natural_v2_accepted_base.nds'
    assert manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['batches'] == previous['batches'] and len(manifest['batches']) == 471
    assert manifest['required_batches'] == [] and all(manifest['checks'].values())
    assert len(registry['accepted_layers']) == 114
    restored = {**registry, 'profiles': {k: v for k, v in registry['profiles'].items() if k != 'all-routes-unified-v1166'}}
    assert restored == prior
    old, new = map(NdsImage.open, (OLD, ROM))
    assert [path for _, path, raw in old.iter_files() if new.read_file(path) != raw] == ['/COMMON/MESFILE.DK4']
    for field in ('arm7', 'arm9OverlayTable', 'arm7OverlayTable'):
        assert getattr(old.rom, field) == getattr(new.rom, field)
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    assert common == (ROOT/'target_COMMON.bin').read_bytes() and arm == (ROOT/'target_ARM9.bin').read_bytes()
    config = read(owned.CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    before = parent.current_entries(old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin'))
    after = owned.current_entries(common, arm)
    rows = {r['message_id']: r for r in read(config['manuscript'])['records']}
    assert len(before) == len(after) == 3668 and tuple(rows) == IDS
    actual_changed, moved = [], []
    for old_row, new_row in zip(before, after, strict=True):
        n = old_row.message_id
        assert new_row.message_id == n
        assert new_row.text == (compiled(rows[n]) if n in rows else old_row.text)
        if old_row.text != new_row.text:
            assert n in rows
            actual_changed.append(n)
        if (old_row.block, old_row.record_index, old_row.block_offset) != (new_row.block, new_row.record_index, new_row.block_offset):
            assert 1756 <= n <= 2099
            moved.append({'ID': n, 'old_block_record_offset': [old_row.block, old_row.record_index, old_row.block_offset],
                          'new_block_record_offset': [new_row.block, new_row.record_index, new_row.block_offset]})
    assert len([r for r in after if r.message_id not in rows]) == 3635
    assert all(before[n].text == after[n].text for n in (676, 677, *range(614, 629), *range(1911, 1931)))
    plan = read(ROOT/'repack_plan.json')
    restored_arm, old_arm = bytearray(arm), old.read_file('/__arm9__.bin')
    for at, size in [*plan['metadata_fields'], *plan['owned_ARM9_fields']]:
        restored_arm[at:at+size] = old_arm[at:at+size]
    assert bytes(restored_arm) == old_arm
    assert arm[:0x800] == old_arm[:0x800]
    builder = Path('scripts/build_integrated_release.py').read_bytes()
    block = (ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert builder.replace(block, b'', 1) == (ROOT/'builder_before.py').read_bytes()
    copies = read(config['native_copy_proof'])
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 180
    assert copies['COMMON_sha256'] == sha(common) and copies['ARM9_sha256'] == sha(arm)
    assert plan['all_sections_BSS_cache_allocations_arenas_and123040_staged_bytes_exact']
    save(ROOT/'physical_record_relocation_verification.json', {'all3668_original_IDs_preserved': True,
        'actual_changed_message_IDs': actual_changed, 'physical_movements': moved,
        'all3635_unselected_texts_and_all_unowned_opaque_payloads_exact': True,
        'opaque_executable_prefix_and_carrier1931_hash_checked_not_padding': True})
    patch, rebuilt, clean = ROM.with_suffix('.xdelta'), ROOT/'patch_reconstruction_RESEARCH_ONLY.nds', Path('work/clean.nds')
    assert not patch.exists() and not rebuilt.exists()
    clean_sha = sha(clean.read_bytes())
    assert clean_sha == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes() and sha(clean.read_bytes()) == clean_sha
    save(proof_path, {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'canonical_base': manifest['base_rom'], 'canonical_sha256': manifest['base_sha256'], 'profile': manifest['profile'],
        'manifest': str(ROM.with_suffix('.manifest.json')), 'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm),
        'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'clean_input_sha256': clean_sha,
        'exact_clean_input_patch_reconstruction': str(rebuilt), 'whole_reconstruction_sha256': sha(rebuilt.read_bytes()),
        'complete_reconstruction_byte_exact': True,
        'all471_batches114_accepted_layers_and_final_guards_pass': True,
        'all33_reviewed_IDs_have_exact_compiler_bytes_and_all3635_unselected_texts_exact': True,
        'all_graphics_routes_fonts_other_ROM_files_ARM7_and_overlays_exact': True,
        'only_COMMON20_22_metadata_DA28_and_existing_escape_bank_status_literal_changed': True,
        'all_boot_prefix_section_BSS_arena_cache_allocations_and123040_staged_bytes_exact': True,
        'all7336_native_copies180_sequences_and_final53_scope36_font_bindings_pass': True,
        'prior_builder_restores_by_removing_exact_optional_block': True,
        'actual_startup_duel_cache_visibility_UI_dismissal_and_transitions_pending': True,
        'inherited_sighting_close_range_name_UI_and_successful_shot_still_pending': True,
        'no_new_completed_editorial_credit_and_canonical_not_promoted': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V1166 combined ancestry and exact clean-input patch verified. Actual startup/duels/transitions pending.', flush=True)
    print('ROM SHA256', manifest['candidate_sha256'])
    print('Patch SHA256', sha(patch.read_bytes()))


if __name__ == '__main__':
    main()
