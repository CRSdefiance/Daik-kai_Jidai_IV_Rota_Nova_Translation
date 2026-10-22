"""Verify the registered full-stack ROM,all unselected bytes and an exact clean-input patch."""
from pathlib import Path

from dk4tool.patch import activity_special_editorial_v987b as parent
from dk4tool.patch import battle_declaration_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta, apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.battle_declaration_layout_v996 import compiled, IDS
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v997b')
OLD = Path('out/all_routes_combined_v987_candidate.nds')
ROM = Path('out/all_routes_combined_v997_candidate.nds')


def main():
    final = ROOT/'registered_release_verification.json'
    assert not final.exists()
    registry = read('translations/release_stack.json')
    prior = read(ROOT/'registry_before.json')
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['profile'] == 'all-routes-unified-v997'
    assert manifest['base_rom'] == 'out\\raphael_natural_v2_accepted_base.nds'
    assert manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(manifest['batches']) == 471 and manifest['required_batches'] == []
    assert all(manifest['checks'].values()) and len(registry['accepted_layers']) == 114
    assert registry['accepted_layers'] == prior['accepted_layers'] and registry['canonical_baseline'] == prior['canonical_baseline']
    assert registry['profiles']['all-routes-unified-v987'] == prior['profiles']['all-routes-unified-v987']
    old, new = map(NdsImage.open, (OLD, ROM))
    changed = [path for _, path, raw in old.iter_files() if new.read_file(path) != raw]
    assert changed == ['/COMMON/MESFILE.DK4']
    for field in ('arm7', 'arm9OverlayTable', 'arm7OverlayTable'):
        assert getattr(old.rom, field) == getattr(new.rom, field)
    common, arm = new.read_file('/COMMON/MESFILE.DK4'), new.read_file('/__arm9__.bin')
    assert common == (ROOT/'target_COMMON.bin').read_bytes() and arm == (ROOT/'target_ARM9.bin').read_bytes()
    config = read(owned.CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    before = parent.current_entries(old.read_file('/COMMON/MESFILE.DK4'), old.read_file('/__arm9__.bin'))
    after = owned.current_entries(common, arm)
    assert len(before) == len(after) == 3668
    assert [a.message_id for a, b in zip(before, after, strict=True) if a.text != b.text] == list(IDS)
    doc = read(config['manuscript'])
    rows = {row['message_id']: row for row in doc['records']}
    for a, b in zip(before, after, strict=True):
        assert (a.message_id, a.record_index) == (b.message_id, b.record_index)
        assert b.text == (compiled(rows[b.message_id]) if b.message_id in rows else a.text)
    assert len([row for row in after if row.message_id not in rows]) == 3646
    assert before[676].text == after[676].text and before[677].text == after[677].text
    assert all(b'\n' not in after[n].text for n in IDS)
    builder = Path('scripts/build_integrated_release.py').read_bytes()
    block = (ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert builder.replace(block, b'', 1) == (ROOT/'builder_before.py').read_bytes()
    copies = read(ROOT/'native_copy_proof.json')
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 178
    assert copies['COMMON_sha256'] == sha(common) and copies['ARM9_sha256'] == sha(arm)
    plan = read(ROOT/'repack_plan.json')
    assert plan['all_sections_BSS_cache_arenas_and_entire123040_staged_payload_unchanged']
    patch, result, clean = ROM.with_suffix('.xdelta'), ROOT/'patch_reconstruction_RESEARCH_ONLY.nds', Path('work/clean.nds')
    assert not patch.exists() and not result.exists()
    clean_sha = sha(clean.read_bytes())
    assert clean_sha == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, result)
    assert result.read_bytes() == ROM.read_bytes()
    assert sha(clean.read_bytes()) == clean_sha
    save(final, {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
        'canonical_base': manifest['base_rom'], 'canonical_sha256': manifest['base_sha256'],
        'profile': manifest['profile'], 'manifest': str(ROM.with_suffix('.manifest.json')),
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'all471_batches114_accepted_layers_and_final_guards_pass': True,
        'only_COMMON_and_proven_ARM9_metadata_runtime_changes_from_V987': True,
        'all3646_unselected_message_strings_and_user676_677_repair_exact': True,
        'all_graphics_routes_names_fonts_other_ROM_files_ARM7_and_overlays_exact': True,
        'all22_one_paragraphs_source_exact_and_no_LF_before_macro_expansion': True,
        'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm),
        'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()), 'clean_input_sha256': clean_sha,
        'exact_clean_input_patch_reconstruction': str(result), 'whole_reconstruction_sha256': sha(result.read_bytes()),
        'complete_reconstruction_byte_exact': True,
        'all7336_native_copies178_cache_sequences_and_owned_footprints_pass': True,
        'prior_builder_restores_by_removing_exact_optional_block': True,
        'startup_actual_UI_RGB_choices_dismissal_and_scene_returns_pending': True,
        'no_new_completed_editorial_credit': True, 'canonical_not_promoted': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V997 verified:22 paragraphs,3646 unselected strings/all unrelated files preserved;471 batches114 accepted layers;exact clean-input patch reconstructs every ROM byte. Actual scenes remain pending.', flush=True)
    print('ROM SHA256', manifest['candidate_sha256'])
    print('Patch SHA256', sha(patch.read_bytes()))


if __name__ == '__main__':
    main()
