"""Record the source-proven actual map mask without changing historical scopes."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_worldmap_overlays_v638 import CAP, ROM
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save
from scripts.verify_worldmap_mask_v639 import ROOT

DOC = Path('docs/worldmap_mask_v639_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V639 World Map mask')
KEY = 'actual_World_Map_original_mask_builder_area_bits_and_cache_lifecycle_v639'


def main():
    proof_path = ROOT / 'native_mask_proof.json'
    proof = read(proof_path)
    assert sha(ROM.read_bytes()) == proof['candidate_sha256']
    assert sha(Path('scripts/verify_worldmap_mask_v639.py').read_bytes()) == proof['script_sha256']
    assert len(proof['three_complete_native_mask_and_copy_cases']) == 3
    assert len(proof['all24_actual_area_records']) == 24
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before_path = ROOT / 'release_and_audit_before.json'
    if not before_path.exists():
        save(before_path, {
            'audits': {name: read(Path('translations') / name) for name in frozen},
            'release_artifacts': {str(p): sha(p.read_bytes()) for p in (
                ROM, ROM.with_suffix('.xdelta'), ROM.with_suffix('.manifest.json'),
                Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds'))}})
    before = read(before_path)
    for path, digest in before['release_artifacts'].items():
        assert sha(Path(path).read_bytes()) == digest
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, before_path, Path('scripts/verify_worldmap_mask_v639.py'), Path(__file__),
             ROOT / 'initial_mask_probe.json', ROOT / 'corrected_mask_probe.json',
             Path(proof['derived_review_sheet']), ROM.with_suffix('.manifest.json'),
             Path(proof['source_composition_proof']), Path(proof['source_capture_report'])]
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    screenshot = CAP / 'frame_036000_final.png'
    checked_copy(screenshot, ARCHIVE / 'REUSED_V638_ORDINARY_V636_frame036000_UNMODIFIED_NATIVE.png')
    save(ARCHIVE / 'provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'reuses_V638_capture_not_a_new_emulator_run': True,
        'reused_unmodified_screen_sha256': sha(screenshot.read_bytes()),
        'controlled_area_bits_and_cache_invalidation_only_in_isolated_native_copies': True,
        'no_extra_guide_candidate_created_from_repeated_screen': True,
        'publication_approved': False, 'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'observed_current_map_mask_construction_gap_from_V551_V638_resolved': True,
        'all24_area_records_and_original_visibility_bit_bindings_verified': True,
        'all28_actual_native_rectangles_match_independent_world_to_pixel_model': True,
        'all19520_actual_packed_bytes_and39040_indices_match_original_native_rebuild': True,
        'three_complete_native_mask_and_copy_cases': True,
        'original_source_setters_bounded_cache_hits_poison_rebuilds_copy_guards_and_ABI_pass': True,
        'all_executed_instruction_words_match_clean': True,
        'existing_actual_V638_screen_and_VRAM_composition_proof_bound_by_hash': True,
        'reuses_existing_capture_no_new_emulator_or_earned_discovery_claim': True,
        'other_actual_pages_sepia_legacy_and_remaining_graphics_gates_open': True,
        'all18_plaque_entries_incomplete_all22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False, 'canonical_promoted': False,
    }
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in before['audits'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        assert all(read(path)[k] == v for k, v in before['audits'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V639: original World Map mask construction and cache lifecycle'
    addition = '''

The observed-state mask gap retained by V551/V638 is resolved. Original native
code rebuilds every19520 packed byte/39040 index from source page7 and24 actual
area-bit records. All28 erasure rectangles match an independent world-to-pixel
model:28865 cleared pixels plus501 retained source zeros account for all29366
background pixels. Actual-state, one-bit and all24-bit native controls pass full
ABI/source-code checks, bounded original setter writes, poisoned scratch/target,
cache invalidation/hit semantics and adjacent guards. Controls remain isolated
native copies, never emulator/save mutations or earned discovery. Proofs and
derived review saved on E; reused V638 screen is labeled, with no new-run claim.
No ROM/patch/registry or release pointer changes. All18 plaques incomplete and22
historical scopes exact;other actual map pages,sepia/legacy and remaining graphics
gates stay open. Full goal active. See [V639 checkpoint](worldmap_mask_v639_checkpoint.md).
'''
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n' + addition, encoding='utf-8')
    print('V639 mask proof and review archived on E;3 audits updated;all18/22 scopes and all release artifacts preserved.')


if __name__ == '__main__':
    main()
